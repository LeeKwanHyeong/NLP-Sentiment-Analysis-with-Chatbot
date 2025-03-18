from nltk.corpus import stopwords
#Train, Test, 토큰화
import pandas as pd
from konlpy.tag import Okt
okt=Okt()
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from keras.models import model_from_json
stopwords = ['도', '는', '다', '의', '가', '이', '은', '한', '에', '하', '고', '을', '를', '인', '듯', '과', '와', '네', '들', '듯', '지', '임', '게','요','거','로','으로',
            '것','수','할','하는','제','에서','그','데','번','해도','죠','된','건','바','구','세']

train_data=pd.read_pickle("c:/data/Train_data.pkl")
test_data=pd.read_pickle("c:/data/Test_data.pkl")
X_Train=train_data['tokenized'].values
Y_Train=train_data['label'].values
X_Test=test_data['tokenized'].values
Y_Test=test_data['label'].values
tokenizer=Tokenizer()
tokenizer.fit_on_texts(X_Train)
vocab_size=19249
tokenizer=Tokenizer(vocab_size,oov_token='OOV')
tokenizer.fit_on_texts(X_Train)
X_Train=tokenizer.texts_to_sequences(X_Train)
X_Test=tokenizer.texts_to_sequences(X_Test)
max_len=100
X_Train=pad_sequences(X_Train,maxlen=max_len)
X_Test=pad_sequences(X_Test,maxlen=max_len)

json_file=open("c:/data/model.json","r")
loaded_model_json=json_file.read()
json_file.close()
loaded_model=model_from_json(loaded_model_json)
loaded_model.load_weights("c:/data/best_model_GRU.h5")
loaded_model.compile(optimizer='rmsprop',loss='binary_crossentropy',metrics=['acc'])

def GRU_predict(new_sentence):
    max_len=90
    new_sentence=okt.morphs(new_sentence)
    new_words=[word for word in new_sentence if not word in stopwords]
    encoded=tokenizer.texts_to_sequences([new_sentence])
    pad_new=pad_sequences(encoded,maxlen=max_len)
    score=float(loaded_model.predict(pad_new))
    percentage=score*100
    return percentage,new_words


def classify_review(sentences):
    percentage,word=GRU_predict(sentences)
    if(((percentage<90.0) and (percentage>5.0))) and (len(word)>6):
        return True
    else:
        return False