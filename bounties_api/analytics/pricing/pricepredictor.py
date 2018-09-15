import re
import numpy as np
# needed for retraining
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import accuracy_score
# from sklearn.metrics import mean_squared_error
import nltk
from nltk.corpus import stopwords
from gensim.models.doc2vec import TaggedDocument, Doc2Vec
from gensim.utils import simple_preprocess
from gensim.models import Word2Vec
from datetime import datetime
import pickle

class PricePredictor:
    """
    this class implments a simple interface to predict a Bounty price
    based on its description, deadline, categories, token type difficulty,
    issue type and platform.
    """
    # regexes for text cleaning
    nonwords = re.compile('[^a-zA-Z \n]')
    double_space = re.compile('\ {2,}')
    double_newline = re.compile("\n{2,}")
    urls = re.compile("https?://[0-9a-zA-Z\-\.\/\?\&\=]+")

    # categorical variables definitions for one-hot encoding
    platforms = ['colorado', 'hiring', 'bounties-network', 'gitcoin']
    bounty_types = ['Code Review', None, 'Documentation', 'Bug',
        'Improvement', 'Feature', 'Other', 'Security', 'Andere']
    experience_levels = ['Beginner', None, 'Intermediate', 'Mittlere', 'Advanced']
    tokens = ['LOVE', 'GIFT', 'GEN', 'WYV', 'DAI', 'ADT', 'AION', 'ETH',
    'COLO', 'ANT', 'BNFT', 'CLN', 'ZRX', 'KIWI', 'LPT', 'TRX', 'MANA', 'AVO']


    def __init__(self):
        self.categories_w2vmodel = Word2Vec.load("data/categories_w2v.pkl")
        self.titles_w2vmodel = Word2Vec.load("data/titles_w2v.pkl")
        self.description_w2vmodel = Word2Vec.load("data/description_w2v.pkl")
        self.description_d2vmodel = doc2vec.load("data/description_d2v.pkl")
        self.prediction_model = pickle.load(open("dats/elasticnet_model.pkl"))
        # or:
        # self.prediction_model = pickle.load(open("dats/xgboost_model.pkl"))
        nltk.download('stopwords')
        return

    def clean_text(text):
        urls_removed = urls.sub('', row).lower()
        non_markdown = nonwords.sub(' ', urls_removed)
        single_space = double_space.sub(' ', non_markdown)
        single_newline = double_newline.sub('\n', single_space)
        description_list = single_newline.split(" ")
        filtered_words = [word for word in description_list if word not in stopwords.words('english')]
        return " ".join(filtered_words)

    def tag_doc(text, platform):
        return TaggedDocument(words=simple_preprocess(text), tags=[platform])

    # Copied from Notebook for future work on retraining models
    # def train_doc2vec_model(tagged_docs, window, size):
    #     sents = tagged_docs.values
    #     doc2vec_model = Doc2Vec(sents, size=size, window=window, iter=20, dm=1)
    #     return doc2vec_model
    #
    # def vec_for_learning(doc2vec_model, tagged_docs):
    #     sents = tagged_docs.values
    #     targets, regressors = zip(*[(doc.tags[0], doc2vec_model.infer_vector(doc.words, steps=20)) for doc in sents])
    #     return targets, regressors
    #
    # def train_w2v_models():
    #     categories_w2vmodel = gensim.models.Word2Vec([x for x in fulfilled_bounties_raw.data_categories_clean], size=100,
    #                                          min_count=3, workers=4)
    #     titles_w2vmodel = gensim.models.Word2Vec([x.split() for x in fulfilled_bounties_raw.title_clean], size=350,
    #                                          min_count=3, workers=4)
    #     description_w2vmodel = gensim.models.Word2Vec([x.split() for x in fulfilled_bounties_raw.description_clean], size=350,
    #                                          min_count=3, workers=4)
    #     return (categories_w2vmodel, titles_w2vmodel, description_w2vmodel)

    # this function averages words by by looking them up in a w2v model
    def average_categories_w2v_array(words):
        try:
            running_total = categories_w2vmodel.wv[words[0]]
        except (KeyError, IndexError):
            return np.zeros((100,))
        for w in words[1:]:
            try:
                this_w = categories_w2vmodel.wv[w]
            except KeyError:
                continue
            running_total = (running_total + this_w)/2
        return running_total

    def average_titles_w2v_array(words):
        s = words.split()
        try:
            running_total = titles_w2vmodel.wv[s[0]]
        except (KeyError, IndexError):
            return np.zeros((350,))
        for w in s[1:]:
            try:
                this_w = titles_w2vmodel.wv[w]
            except KeyError:
                continue
            running_total = (running_total + this_w)/2
        return running_total

    def average_description_w2v_array(words):
        s = words.split()
        try:
            running_total = description_w2vmodel.wv[s[0]]
        except (KeyError, IndexError):
            return np.zeros((350,))
        for w in s[1:]:
            try:
                this_w = description_w2vmodel.wv[w]
            except KeyError:
                continue
            running_total = (running_total + this_w)/2
        return running_total

    def get_one_hot(targets, nb_classes):
        res = np.eye(nb_classes)[np.array(targets).reshape(-1)]
        return res.reshape(list(targets.shape)+[nb_classes])

    def get_days_to_deadline(deadline):
        # implement some cleanup logic in time windows
        # negative deadlines are mistakes due to API changes
        days_to_deadline = (deadline - datetime.now()).days
        if days_to_deadline < 0:
            return 0
        # assume that anything > 5y is infinte
        if days_to_deadline > 5*365:
            return 0
        return days_to_deadline

    def get_doc2_vec_array(self, platform, description_clean):
        tagged_doc = tag_doc(description_clean, platform)
        targets, regressors = (platform, self.description_d2vmodel.infer_vector(tagged_doc.words, steps=20))
        return (targets, regressors)

    def generate_feature_array(self, description, title, categories, deadline_timestamp, experience_level,
                              difficulty, deadline, token_type, platform):
        # munge timestamp
        days_to_deadline = get_days_to_deadline(deadline_timestamp)
        # apply text cleaning
        description_clean = clean_text(description)
        description_length = len(description.split())
        title_clean = clean_text(title)
        data_categories_clean = [x.strip().lower() for x in categories]

        # first, doc2vec of description
        new_row = get_doc2_vec_array(description_clean) # doc2vec of desc.
        new_row = np.concatenate((new_row, np.array([days_to_deadline, description_length])), axis = None)

        # categorical features (one-hot encoded)
        el_one_hot = get_one_hot(np.array(self.experience_levels.index(experience_level)), len(self.experience_levels))
        bt_one_hot = get_one_hot(np.array(self.bounty_types.index(bounty_type)), len(self.bounty_types))
        pl_one_hot = get_one_hot(np.array(self.platforms.index(platform)), len(self.platforms))
        ts_one_hot = get_one_hot(np.array(self.tokens.index(token_type), len(self.tokens))
        new_row = np.concatenate((new_row, el_one_hot, bt_one_hot, pl_one_hot, ts_one_hot), axis = None)

        # w2v features
        new_row = np.concatenate((new_row, average_categories_w2v_array(data_categories_clean)), axis = None)
        new_row = np.concatenate((new_row, average_titles_w2v_array(title_clean)), axis = None)
        new_row = np.concatenate((new_row, average_description_w2v_array(description_clean)), axis = None)

        # all done!
        new_row.shape = (1,1138)
        return new_row

    def predict(self, title, description, categories, difficulty,
                revisions, deadline, token_type, platform):
        # TODO: use loaded w2v and d2v models to generate matrix
        pass

    def retrain():
        raise NotImplementedError("Not implemented yet!")
