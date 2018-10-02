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
    nonwords = re.compile(r'[^a-zA-Z \n]')
    double_space = re.compile(r'\ {2,}')
    double_newline = re.compile(r'\n{2,}')
    urls = re.compile(r'https?://[0-9a-zA-Z\-\.\/\?\&\=]+')

    # categorical variables definitions for one-hot encoding
    platforms = ['colorado', 'hiring', 'bounties-network', 'gitcoin']
    bounty_types = ['Code Review', None, 'Documentation', 'Bug',
                    'Improvement', 'Feature', 'Other', 'Security', 'Andere']
    experience_levels = ['Beginner', None,
                         'Intermediate', 'Mittlere', 'Advanced']
    tokens = ['LOVE', 'GIFT', 'GEN', 'WYV', 'DAI', 'ADT', 'AION', 'ETH',
              'COLO', 'ANT', 'BNFT', 'CLN', 'ZRX', 'KIWI', 'LPT', 'TRX', 'MANA', 'AVO']

    def __init__(self):
        self.categories_w2vmodel = Word2Vec.load("data/categories_w2v.pkl")
        self.titles_w2vmodel = Word2Vec.load("data/titles_w2v.pkl")
        self.description_w2vmodel = Word2Vec.load("data/description_w2v.pkl")
        self.description_d2vmodel = Doc2Vec.load("data/description_d2v.pkl")
        self.prediction_model = pickle.load(open("data/elasticnet_model.pkl", 'rb'))
        # or:
        # self.prediction_model = pickle.load(open("dats/xgboost_model.pkl"))
        nltk.download('stopwords')
        return

    def clean_text(self, text):
        """ Strip URLs, extra space, non-alnum and stopwords from a text """
        urls_removed = self.urls.sub('', text).lower()
        non_markdown = self.nonwords.sub(' ', urls_removed)
        single_space = self.double_space.sub(' ', non_markdown)
        single_newline = self.double_newline.sub('\n', single_space)
        description_list = single_newline.split(" ")
        filtered_words = [
            word for word in description_list if word not in stopwords.words('english')]
        return " ".join(filtered_words)

    def tag_doc(self, text, platform):
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
    def average_categories_w2v_array(self, words):
        """ Determine the average vector for a list of categories """
        try:
            running_total = self.categories_w2vmodel.wv[words[0]]
        except (KeyError, IndexError):
            return np.zeros((100,))
        for w in words[1:]:
            try:
                this_w = self.categories_w2vmodel.wv[w]
            except KeyError:
                continue
            running_total = (running_total + this_w) / 2
        return running_total

    def average_titles_w2v_array(self, words):
        """ Determine the average vector for a title """
        s = words.split()
        try:
            running_total = self.titles_w2vmodel.wv[s[0]]
        except (KeyError, IndexError):
            return np.zeros((350,))
        for w in s[1:]:
            try:
                this_w = self.titles_w2vmodel.wv[w]
            except KeyError:
                continue
            running_total = (running_total + this_w) / 2
        return running_total

    def average_description_w2v_array(self, words):
        """ Determine the average vector for a description """
        s = words.split()
        try:
            running_total = self.description_w2vmodel.wv[s[0]]
        except (KeyError, IndexError):
            return np.zeros((350,))
        for w in s[1:]:
            try:
                this_w = self.description_w2vmodel.wv[w]
            except KeyError:
                continue
            running_total = (running_total + this_w) / 2
        return running_total

    def get_one_hot(self, targets, nb_classes):
        """ One hot encode categorical variables """
        res = np.eye(nb_classes)[np.array(targets).reshape(-1)]
        return res.reshape(list(targets.shape) + [nb_classes])

    def get_days_to_deadline(self, deadline):
        """ Take a timestamp and convert it to days from now, then bin it """
        # implement some cleanup logic in time windows
        # negative deadlines are mistakes due to API changes
        days_to_deadline = (deadline - datetime.now()).days
        if days_to_deadline < 0:
            return 0
        # assume that anything > 5y is infinte
        if days_to_deadline > 5 * 365:
            return 0
        return days_to_deadline

    def get_doc2_vec_array(self, platform, description_clean):
        """ Get the doc2vec array for a new text from
        from the saved description d2v model """
        tagged_doc = self.tag_doc(description_clean, platform)
        targets, regressors = (
            platform, self.description_d2vmodel.infer_vector(tagged_doc.words, steps=20))
        return (targets, regressors)

    def generate_feature_array(self, title, description, categories, experience_level, deadline_timestamp,
                               token_type, bounty_type, platform):
        """ Returns a feature vector for input into a sklearn predictor """
        # munge timestamp
        days_to_deadline = self.get_days_to_deadline(deadline_timestamp)
        # apply text cleaning
        description_clean = self.clean_text(description)
        description_length = len(description.split())
        title_clean = self.clean_text(title)
        data_categories_clean = [x.strip().lower() for x in categories]

        # first, doc2vec of description
        # doc2vec of desc.
        new_row = self.get_doc2_vec_array(platform, description_clean)[1]
        new_row = np.concatenate(
            (new_row, np.array([days_to_deadline, description_length])), axis=None)

        # categorical features (one-hot encoded)
        el_one_hot = self.get_one_hot(np.array(self.experience_levels.index(
            experience_level)), len(self.experience_levels))
        bt_one_hot = self.get_one_hot(
            np.array(self.bounty_types.index(bounty_type)), len(self.bounty_types))
        pl_one_hot = self.get_one_hot(
            np.array(self.platforms.index(platform)), len(self.platforms))
        ts_one_hot = self.get_one_hot(
            np.array(self.tokens.index(token_type)), len(self.tokens))
        new_row = np.concatenate(
            (new_row, el_one_hot, bt_one_hot, pl_one_hot, ts_one_hot), axis=None)

        # w2v features
        new_row = np.concatenate(
            (new_row, self.average_categories_w2v_array(data_categories_clean)), axis=None)
        new_row = np.concatenate(
            (new_row, self.average_titles_w2v_array(title_clean)), axis=None)
        new_row = np.concatenate(
            (new_row, self.average_description_w2v_array(description_clean)), axis=None)

        # all done!
        new_row.shape = (1, 1138)
        return new_row

    def predict(self, title, description, categories, experience_level,
                deadline, token_type, bounty_type, platform):
        """ Predicts a closing price (in USD) for a bounty """
        features = self.generate_feature_array(title, description, categories,
                                               experience_level, deadline, token_type, bounty_type, platform)
        result = self.prediction_model.predict(features)
        if result < 0:
            return 0
        return result

    def retrain(self):
        raise NotImplementedError("Not implemented yet!")
