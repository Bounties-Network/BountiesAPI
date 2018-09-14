# Predicting bounty price based on issue text

## Abstract

The goal of this work is to predict a bounty's closing price based on the
textual content of the bounty. The main hypothesis is that an issue's text is
able to predict its price. As it turns out, this is only partially true, and
there are some features (token type, description length, and categories) that
explain some of the variance in the pricing. These hint at a number of areas
which may be very useful in the future to help curate a great market.

## Methods

1. Load all bounties from `pg_dump` of `bounties` database, derived from
`contract_subscriber`.
2. Filter un-closed and small bounties (< 10$ currently)
3. Feature generation: bounty description text cleaning
  1. Strip stopwords using `nltk`s English stopwords file
  2. Replace non-alnum characters and URLs
  3. Strip all repeated spacing characters (but retaining `\ ` and `\n`)
  4. Convert all letters to lowercase
4. Feature generation for titles and descriptions
  1. Convert all characters to lowercase
  2. Strip all leading and trailing and repeated spaces
5. Other categorical variables (bounty type, difficulty level,
token type, bounty platform)
6. Compute days to deadline, replacing null
deadlines with 0
7. Compute doc2vec model for description, word2vec model for
description, title and categories. Compute description length in words.
8. Create matrix, split for training/testing 80%/20%
9. 9. Grid search and optimal model selection. Compared:
  1. Gradient Boosted Trees (`XGBoost`)
  2. Random Forests (`sklearn`)
  3. Linear regression (`sklearn`)
  4. Lasso regression (`sklearn`)
  5. Ridge regression (`sklearn`)
  6. Elastic Net regression (`sklearn`)

## Results

Gradient Boosting and Elastic Net performed the best. MSE was chosen as the
distance metric to evaluate test data fraction.

Show figures about bounties and prices

## Discussion

### Short and Long descriptions appear to result in expensive bounties

Example: Reddit Bot bounty

### Data insufficiency is a challenge

Discuss figures

### Tokens explain a lot of the price variablity, since we fit on USD

Could use other stablecoin or ETH but need a common denominator. Alternatively
produce models for each coin (though including this feature already kinda does
that). Could also produce multiple predictions (instead of just one, in this
case, USD)

### NLP might not be the best option right now, ecnometric approahes are likely
### better for the platform now

When there are more bounties it will work better, but I believe in the short
term a statistical approach that works on percentile is probably the best
choice. Would suggest slicing by category (if big enough) and
log-normalized-and-binned days to deadline.

## Future research

1. RNN/CNN on text
2. More rigorous grid search
3. Just... rerun everything here with more data. It's state of the art NLP.
4. Language detection, although only needed when someone posts a non-English
bounty
5. Design platform protocol to collect more machine-friendly data.
E.g.: enforce a more strict category system, encode features like programming
language, frameworks or toolkits.
6. Better error metrics compared to MSE.
7. Look into who's submitting bounties, consider this more than not at all.
