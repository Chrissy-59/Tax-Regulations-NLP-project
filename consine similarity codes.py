from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

doc_1 = "Mr. Trump became president after winning the political election. Though he lost the support of some republican friends, Trump is friends with President Putin"
doc_2 = "President Trump says Putin had no political interference is the election outcome. He says it was a witchhunt by political parties. He claimed President Putin is a friend who had nothing to do with the election"

##Porter stem
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
ps = PorterStemmer()
def stemSentence(sentence):
    token_words=word_tokenize(sentence)
    token_words
    stem_sentence=[]
    for word in token_words:
        stem_sentence.append(ps.stem(word))
        stem_sentence.append(" ")
    return "".join(stem_sentence)


documents = [doc_1, doc_2]

# option 1 : use CountVectorizer
# Create the Document Term Matrix
count_vectorizer = CountVectorizer(stop_words='english')
count_vectorizer = CountVectorizer()
cv_matrix = count_vectorizer.fit_transform(documents)
doc_term_matrix_cv = cv_matrix.todense()

# OPTIONAL: Convert Sparse Matrix to Pandas Dataframe if you want to see the word frequencies.
df_cv = pd.DataFrame(doc_term_matrix_cv,
                     columns=count_vectorizer.get_feature_names(),
                     index=['doc_1', 'doc_2'])

# print(cosine_similarity(df_cv))
cs_cv = cosine_similarity(doc_term_matrix_cv)
cs_cv_score = cs_cv[0, 1]
print(cs_cv_score)

# option2 :  use TfidfVectorizer
tfidf_vectorizer = TfidfVectorizer(stop_words='english')
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(documents)
doc_term_matrix_tfidf = tfidf_matrix.todense()
cs_tv = cosine_similarity(doc_term_matrix_tfidf)
cs_tv_score = cs_tv[0, 1]
print(cs_tv_score)
