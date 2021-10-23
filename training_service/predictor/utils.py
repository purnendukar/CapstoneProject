from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

import pickle
import re


def text_preprocessor(text):
    stemmer=PorterStemmer()
    sents=' '.join([sent for sent in sent_tokenize(text)])
    words=[word for word in word_tokenize(sents) if not word in stopwords.words('english')]
    words=[word for word in words if len(word)>1]
    #words=[word for word in words if not word in punctuation]
    words=[re.sub('[^a-zA-Z]+', '',word) for word in words]
    #tagged_words=[nltk.pos_tag(word) for word in words]
    words=' '.join([stemmer.stem(word) for word in words])
    vectroizer=pickle.load(open('./models/tfidfvectorizer.pkl','rb'))
    transformed=vectroizer.transform([words])
    return transformed


def predictor(transformed_text):
    model=pickle.load(open('./models/multinbmodel.pkl','rb'))
    classmapper=pickle.load(open('./models/classmapper.pkl','rb'))
    pred=model.predict(transformed_text)[0]
    #print(pred)
    classname=classmapper.get(pred)
    return classname

def columnmapper(classindex):
    classmapper=pickle.load(open('./models/classmapper.pkl','rb'))
    return classmapper.get(int(classindex))

def retrain_model(rdd):
    rdd=rdd.dropna(how='any')
    rdd=rdd.collect()
    corpus=[]
    topic=[]
    for row in rdd[:]:
        text=row['title']+' '+row['summary']
        #text=row['text']
        corpus.append(text)
        topic.append(row['topic'])
    updated_corpus=[]
    stemmer=PorterStemmer()
    for row in corpus:
        sents=' '.join([sent for sent in sent_tokenize(row)])
        words=[word for word in word_tokenize(sents) if not word in stopwords.words('english')]
        words=[word for word in words if len(word)>1]
        #words=[word for word in words if not word in punctuation]
        words=[re.sub('[^a-zA-Z0-9.]+', '',word) for word in words]
        #tagged_words=[nltk.pos_tag(word) for word in words]
        words=' '.join([stemmer.stem(word) for word in words])
        updated_corpus.append(words)
    vectorizer=pickle.load(open('./models/tfidfvectorizer.pkl','rb'))
    model=pickle.load(open('./models/multinbmodel.pkl','rb'))
    encoder=pickle.load(open('./models/labelencoder.pkl','rb'))
    trans_x=vectorizer.transform(updated_corpus)
    trans_y=encoder.transform(topic)
    model.fit(trans_x,trans_y)
    pickle.dump(model,open('./models/multinbmodel.pkl','wb'))
        