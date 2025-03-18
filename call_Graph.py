import numpy as np
from konlpy.tag import Okt
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.font_manager as fm
okt = Okt()


def call_dict():
    '''read_ne.pkl,read_po,read_with의 저장경로를 삽입.'''

    read_ne_df = pd.read_pickle("C:\\data\\real_ne.pkl")#change
    read_po_df = pd.read_pickle("C:\\data\\real_po.pkl")#change
    read_with_df = pd.read_pickle("C:\\data\\real_with.pkl")#change
    po_word = list(np.array(read_po_df['word']))
    po_weight = list(np.array(read_po_df['weight']))
    ne_word = list(np.array(read_ne_df['word']))
    ne_weight = list(np.array(read_ne_df['weight']))
    with_word = list(np.array(read_with_df['word']))
    with_weight = list(np.array(read_with_df['weight']))
    all_word = po_word + ne_word + with_word
    all_weight = po_weight + ne_weight + with_weight
    all_list = [all_word, all_weight]
    all_dic = dict(zip(*all_list))
    return all_dic


# 들어오는 리뷰들을 지정된 점수로 분류하여 라인별로 묶기.
# 들어오는 리뷰들을 지정된 점수로 분류하여 라인별로 묶기.
def scoring(sentence):
    score, word, weight = [], [], []
    a, b = [], []
    dictionary = call_dict()
    summation = 0
    stopwords = ['도', '는', '다', '의', '가', '이', '은', '한', '에', '하', '고', '을', '를', '인', '듯', '과', '와', '네', '들', '듯',
                 '지', '임', '게', '요', '거', '로', '으로',
                 '것', '수', '할', '하는', '제', '에서', '그', '데', '번', '해도', '죠', '된', '건', '바', '구', '세', '최신', '.']
    word_tokens = okt.morphs(sentence)
    word_tokens = [x for x in word_tokens if x not in stopwords]

    for x in word_tokens:
        if dictionary.get(x):

            if (len(x) == 1):
                continue
            elif (len(x) > 1):
                word.append(x)
                score.append(dictionary[x])
        else:
            continue
    for sc in score:
        summation += sc
    for sc in score:
        weight.append(sc / summation)
    all_list = [word, weight]
    dict_n = dict(zip(*all_list))
    s_dic = sorted(dict_n.items(), key=lambda x: x[1], reverse=True)
    best_dic = s_dic[:10]
    temp_word, temp_weight = [], []
    for split in range(len(best_dic)):
        list_ = list(best_dic[split])
        temp_word.append(list_[0])
        temp_weight.append(list_[1])
    final_list = [temp_word, temp_weight]
    final = dict(zip(*final_list))

    return final


## scoring function을 이용해 csv로 받아온 리뷰를 정렬
##location 매개변수는 메인함수에서 돌릴때 찾아서 변경
def merge_all(data):
    # 데이터프레임으로 된것 저장
    merged = {}
    temp_list = []
    for line in data['content']:
        x = scoring(line)
        temp_list.append(x)
    for mer in range(len(temp_list)):
        merged = {**temp_list[mer], **merged}
    return merged


def wordcloud(df):
    tokens = merge_all(df)
    wordcloud = WordCloud(font_path='C:/Windows/Fonts/malgun.ttf', background_color='white', colormap='Accent_r',
                          width=1500, height=1000).generate_from_frequencies(tokens)
    plt.imshow(wordcloud)
    plt.axis('off')

    plt.show()

def bar_plot(dict1,dict2):

    fl = fm.FontProperties(fname='c:/Windows/Fonts/malgun.ttf').get_name()
    plt.rc('font', family=fl)
    plt.bar(dict1.keys(), dict1.values(),label='Positive', color='b')
    plt.bar(dict2.keys(), dict2.values(),label='Negative', color='r')
    plt.legend()
    plt.title('Count_Positive_Negative')
    plt.show()

