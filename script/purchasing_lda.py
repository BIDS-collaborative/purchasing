import re
import random
import lda
import csv
import pandas as pd
import numpy as np
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer


def main():
    # Load data
    df = pd.read_csv('../../data/cleaned/UCB_dept_merge.csv')

    # Randomly select 20k
    random.seed(8675309)
    rows = random.sample(df.index, 20000)
    df = df.ix[rows].reset_index()

    # Cleaning
    cols = ['supplier_name', 'item_type', 'product_description', 'manufacturer',
            'buyer__first_name', 'buyer__last_name', 'department_name']
    for col in cols:
        df[col] = df[col].replace(np.nan, '' , regex=True)                                      \
                         .apply(lambda x: x.lower())                                            \
                         .apply(lambda x: re.sub('(http\S*|www\S*)', '', x))                    \
                         .apply(lambda x: re.sub('((?<=\D)/|/(?=\D))', ' ', x))                 \
                         .apply(lambda x: re.sub('[^A-Za-z0-9.%\/]+', ' ', x))                  \
                         .apply(lambda x: re.sub('\.+', '', x))                                 \
                         .apply(lambda x: re.sub('(?<=\s)\w(?=\s)|(?<=\s)\d(?=\s)', '', x))     \
                         .apply(lambda x: re.sub('\s+', ' ', x).strip())

    # Product descriptions to list
    pd_list = []
    for i in xrange(0, df.product_description.size):
        pd_list.append(df.product_description[i])

    # Initialize CountVevtorizer, remove stop words
    vectorizer = CountVectorizer(analyzer = "word",
                                 tokenizer = None,
                                 preprocessor = None,
                                 stop_words = 'english')

    # Transform pd_list to a document-term matrix
    X = vectorizer.fit_transform(pd_list).toarray()

    # Unique words
    vocab = vectorizer.get_feature_names()

    # LDA
    model = lda.LDA(n_topics=100, n_iter=1500, random_state=8675309)
    model.fit(X)

    # Output topic definitions to CSV (overwrites existing)
    topic_word = model.topic_word_
    n_top_words = 11
    with open('../../results/topic_definitions.csv', 'wb') as to_:
        writer = csv.writer(to_, delimiter=',', quotechar='\"')
        doc_topic = model.doc_topic_
        for i, topic_dist in enumerate(topic_word):
            topic_words = np.array(vocab)[np.argsort(topic_dist)][:-n_top_words:-1]
            writer.writerow([i, ' '.join(topic_words)])

    # Output purchase description designation to CSV (overwrites existing)
    with open('../../results/pd_topics.csv', 'wb') as to_:
        writer = csv.writer(to_, delimiter=',', quotechar='\"')
        doc_topic = model.doc_topic_
        for i in range(len(pd_list)):
            writer.writerow([pd_list[i], doc_topic[i].argmax()])


if __name__ == '__main__':
    main()