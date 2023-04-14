from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
def cs_cv(doc_1,doc_2):
    documents = [doc_1, doc_2]
    # Create the Document Term Matrix
    count_vectorizer = CountVectorizer(stop_words='english')
    count_vectorizer = CountVectorizer()
    cv_matrix = count_vectorizer.fit_transform(documents)
    doc_term_matrix_cv = cv_matrix.todense()
    cs_cv = cosine_similarity(doc_term_matrix_cv)
    cs_cv_score = cs_cv[0, 1]
    return(cs_cv_score)

# option2 :  use TfidfVectorizer
def cs_tv(doc_1,doc_2):
    documents = [doc_1, doc_2]
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(documents)
    doc_term_matrix_tfidf = tfidf_matrix.todense()
    cs_tv = cosine_similarity(doc_term_matrix_tfidf)
    cs_tv_score = cs_tv[0, 1]
    return(cs_tv_score)