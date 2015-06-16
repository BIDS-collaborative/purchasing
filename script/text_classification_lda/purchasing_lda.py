import re
import random
import lda
import csv
import numpy as np
import pandas as pd
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer


def main():
    # Load data
    df = pd.read_csv('../data/cleaned/UCB_dept_merge.csv')

    # Concatenate supplier name and manufacturer
    df['product_line'] = df['supplier_name'] + ' ' + \
                         df['product_description'] + ' ' + \
                         df['manufacturer']

    # Randomly select 40k
    random.seed(8675309)
    rows = random.sample(df.index, 40000)
    df = df.ix[rows].reset_index()

    # Cleaning
    cols = ['supplier_name', 'item_type', 'product_description', 'manufacturer',
            'buyer__first_name', 'buyer__last_name', 'department_name', 'product_line']
    for col in cols:
        df[col] = df[col].replace(np.nan, '' , regex=True)                                      \
                         .apply(lambda x: x.lower())                                            \
                         .apply(lambda x: re.sub('(http\S*|www\S*)', '', x))                    \
                         .apply(lambda x: re.sub('((?<=\D)/|/(?=\D))', ' ', x))                 \
                         .apply(lambda x: re.sub('[^A-Za-z0-9.%\/]+', ' ', x))                  \
                         .apply(lambda x: re.sub('\.+', '', x))                                 \
                         .apply(lambda x: re.sub('(?<=\s)\w(?=\s)|(?<=\s)\d(?=\s)', '', x))     \
                         .apply(lambda x: re.sub('\s+', ' ', x).strip())

    # Tokenize
    tokenized_pd = [word_tokenize(line) for line in df.product_line]

    # Stop words
    stop_words = stopwords.words('english') + \
                 [u'ea', u'per', u'item', u'description', u'quote', u'pk', u'pack',
                  'give', 'something', 'inc', 'corporation', 'quantity', 'back',
                  'products', 'co', 'officemax', 'unit', 'corp', 'llc', 'new']

    # Remove stop words, numbers, single chars
    tokenized_pd_clean = []
    for entry in tokenized_pd:
        entry_list = []
        for word in entry:
            if ((not word in stop_words) and (not unicode(word).isnumeric()) and (not len(word) <= 1)):
                entry_list.append(word)
        tokenized_pd_clean.append(entry_list)

    # De-tokenize
    pd_list_clean = []
    for item in tokenized_pd_clean:
        pd_list_clean.append(' '.join(item))

    # Initialize CountVectorizer, remove stop words
    vectorizer = CountVectorizer(analyzer = "word", 
                                 tokenizer = None, 
                                 preprocessor = None, 
                                 stop_words = None)

    # Transform pd_list_clean to a document-term matrix
    X = vectorizer.fit_transform(pd_list_clean).toarray()

    # Unique words
    vocab = vectorizer.get_feature_names()

    # Number of topics
    for n_topics in range(5, 16):

        # File names
        t_def_fname = 'topics_definitions_' + str(n_topics) + '.csv'
        t_fname = 'pd_topics_' + str(n_topics) + '.csv'

        # LDA
        model = lda.LDA(n_topics=n_topics, n_iter=1500, random_state=8675309)
        model.fit(X)

        # Output topic definitions to CSV (overwrites existing)
        topic_word = model.topic_word_
        n_top_words = 21
        with open('../results/'+t_def_fname, 'wb') as to_:
            writer = csv.writer(to_, delimiter=',', quotechar='\"')
            doc_topic = model.doc_topic_
            for i, topic_dist in enumerate(topic_word):
                topic_words = np.array(vocab)[np.argsort(topic_dist)][:-n_top_words:-1]
                writer.writerow([i, ' '.join(topic_words)])

        # Output purchase description designation to CSV (overwrites existing)
        with open('../results/'+t_fname, 'wb') as to_:
            writer = csv.writer(to_, delimiter=',', quotechar='\"')
            doc_topic = model.doc_topic_
            for i in range(len(tokenized_pd_clean)):
                writer.writerow([tokenized_pd_clean[i], doc_topic[i].argmax()])


if __name__ == '__main__':
    main()
