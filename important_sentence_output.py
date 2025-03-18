import numpy as np
import pandas as pd
from konlpy.tag import Okt
from collections import Counter
from pykospacing import spacing
import os


# x는 csv 저장 위치
def output_sentence_all(data_frame):
    okt = Okt()
    data = data_frame
    stopwords = ['도', '는', '다', '의', '가', '이', '은', '한', '에', '하', '고', '을', '를', '인', '듯', '과', '와', '네', '들', '듯',
                 '지', '임', '게', '요', '거', '로', '으로',
                 '것', '수', '할', '하는', '제', '에서', '그', '데', '번', '해도', '죠', '된', '건',
                 '바', '구', '세', '랑', '시', '저', '만']
    data['content'] = data['content'].str.replace('[^ㄱ-ㅎㅏ-ㅣ|가-힣]', '')
    data['tokenized'] = data['content'].apply(okt.morphs)
    data['tokenized'] = data['tokenized'].apply(lambda x: [item for item in x if item not in stopwords])
    x = data['tokenized']
    for line in x:
        for word in line:
            if len(word) < 2:
                line.remove(word)
    data['tokenized'] = x

    negative_count = np.hstack(data[data.grade < 3]['tokenized'].values)
    positive_count = np.hstack(data[data.grade > 2]['tokenized'].values)
    negative_word_count = Counter(negative_count)
    positive_word_count = Counter(positive_count)

    negative_test = dict(negative_word_count.most_common(10))
    positive_test = dict(positive_word_count.most_common(10))

    check_negative = []
    check_positive = []

    # 긍정 부정에 대한 문장 추출용 단어집
    for word in negative_test.keys():
        check_negative.append(word)
    for word in positive_test.keys():
        check_positive.append(word)

    # 긍정 부정에 대한 문장 추출 및 중복 제거

    po_sentence, ne_sentence = [], []
    new_po_sen, new_ne_sen = [], []
    # 1)부정
    for num in range(len(data['tokenized'])):
        for token in data['tokenized'][num]:
            if token in check_negative:
                ne_sentence.append(data['content'][num])
    for s in ne_sentence:
        if s not in new_ne_sen:
            new_ne_sen.append(s)

    # 2)긍정
    for num in range(len(data['tokenized'])):
        for token in data['tokenized'][num]:
            if token in check_positive:
                po_sentence.append(data['content'][num])
    for s in po_sentence:
        if s not in new_po_sen:
            new_po_sen.append(s)

    spacing_po,spacing_ne=[],[]

    for line in new_ne_sen:
        spacing_ne.append(spacing(line))
    for line in new_po_sen:
        spacing_po.append(spacing(line))

    spacing_po=pd.Series(spacing_po)
    spacing_ne=pd.Series(spacing_ne)
    extract_df=pd.DataFrame()
    extract_df['positive']=spacing_po
    extract_df['negative']=spacing_ne

    if not os.path.exists('c:/data/extract_.csv'):
        extract_df.to_csv('c:/data/extract_.csv',index=False,mode='w',encoding='utf_8_sig')
    else:
        extract_df.to_csv('c:/data/extract_.csv',index=False,mode='a',encoding='utf_8_sig',header=False)

    return positive_test, negative_test, extract_df

import numpy as np
import pandas as pd
from konlpy.tag import Okt
from collections import Counter
from pykospacing import spacing
import os


# x는 csv 저장 위치
def output_sentence_all(data_frame):
    okt = Okt()
    data = data_frame
    stopwords = ['도', '는', '다', '의', '가', '이', '은', '한', '에', '하', '고', '을', '를', '인', '듯', '과', '와', '네', '들', '듯',
                 '지', '임', '게', '요', '거', '로', '으로',
                 '것', '수', '할', '하는', '제', '에서', '그', '데', '번', '해도', '죠', '된', '건',
                 '바', '구', '세', '랑', '시', '저', '만']
    data['content'] = data['content'].str.replace('[^ㄱ-ㅎㅏ-ㅣ|가-힣]', '')
    data['tokenized'] = data['content'].apply(okt.morphs)
    data['tokenized'] = data['tokenized'].apply(lambda x: [item for item in x if item not in stopwords])
    x = data['tokenized']
    for line in x:
        for word in line:
            if len(word) < 2:
                line.remove(word)
    data['tokenized'] = x

    negative_count = np.hstack(data[data.grade < 3]['tokenized'].values)
    positive_count = np.hstack(data[data.grade > 2]['tokenized'].values)
    negative_word_count = Counter(negative_count)
    positive_word_count = Counter(positive_count)

    negative_test = dict(negative_word_count.most_common(10))
    positive_test = dict(positive_word_count.most_common(10))

    '''check_negative = []
    check_positive = []

    # 긍정 부정에 대한 문장 추출용 단어집
    for word in negative_test.keys():
        check_negative.append(word)
    for word in positive_test.keys():
        check_positive.append(word)

    # 긍정 부정에 대한 문장 추출 및 중복 제거

    po_sentence, ne_sentence = [], []
    new_po_sen, new_ne_sen = [], []
    # 1)부정
    for num in range(len(data['tokenized'])):
        for token in data['tokenized'][num]:
            if token in check_negative:
                ne_sentence.append(data['content'][num])
    for s in ne_sentence:
        if s not in new_ne_sen:
            new_ne_sen.append(s)

    # 2)긍정
    for num in range(len(data['tokenized'])):
        for token in data['tokenized'][num]:
            if token in check_positive:
                po_sentence.append(data['content'][num])
    for s in po_sentence:
        if s not in new_po_sen:
            new_po_sen.append(s)

    spacing_po,spacing_ne=[],[]

    for line in new_ne_sen:
        spacing_ne.append(spacing(line))
    for line in new_po_sen:
        spacing_po.append(spacing(line))

    spacing_po=pd.Series(spacing_po)
    spacing_ne=pd.Series(spacing_ne)
    extract_df=pd.DataFrame()
    extract_df['positive']=spacing_po
    extract_df['negative']=spacing_ne

    if not os.path.exists('c:/data/extract_.csv'):
        extract_df.to_csv('c:/data/extract_.csv',index=False,mode='w',encoding='utf_8_sig')
    else:
        extract_df.to_csv('c:/data/extract_.csv',index=False,mode='a',encoding='utf_8_sig',header=False)'''

    return positive_test, negative_test


def output_sentence_select(data_frame):
    okt = Okt()
    data = data_frame
    stopwords = ['도', '는', '다', '의', '가', '이', '은', '한', '에', '하', '고', '을', '를', '인', '듯', '과', '와', '네', '들', '듯',
                 '지', '임', '게', '요', '거', '로', '으로',
                 '것', '수', '할', '하는', '제', '에서', '그', '데', '번', '해도', '죠', '된', '건',
                 '바', '구', '세', '랑', '시', '저', '만', '너무', '입니다']
    data['content'] = data['content'].str.replace('[^ㄱ-ㅎㅏ-ㅣ|가-힣]', '')
    data['tokenized'] = data['content'].apply(okt.morphs)
    data['tokenized'] = data['tokenized'].apply(lambda x: [item for item in x if item not in stopwords])
    x = data['tokenized']
    for line in x:
        for word in line:
            if len(word) < 2:
                line.remove(word)
    data['tokenized'] = x

    negative_count = np.hstack(data[data.grade < 3]['tokenized'].values)
    positive_count = np.hstack(data[data.grade > 2]['tokenized'].values)
    negative_word_count = Counter(negative_count)
    positive_word_count = Counter(positive_count)

    negative_test = dict(negative_word_count.most_common(10))
    positive_test = dict(positive_word_count.most_common(10))

    return positive_test, negative_test


def filter(data_frame, dictionary):
    first_token, first_sentence, second_token = [], [], []
    word = [x for x in dictionary.keys()]

    final_word, final_sent = [], []
    for index in range(len(data_frame['content'])):
        aa, bb = [], []
        for tok in word:
            if tok in data_frame['tokenized'][index]:
                aa.append(tok)
        bb.append(data_frame['content'][index])
        final_word.append(aa)
        final_sent.append(bb)
    final_sent = pd.Series(final_sent)
    final_word = pd.Series(final_word)
    return final_word, final_sent


def classifying(test):
    a = test
    positive, negative = output_sentence_select(a)
    po_words, po_sentence = filter(a, positive)
    ne_words, ne_sentence = filter(a, negative)

    df = pd.DataFrame()
    se1 = pd.Series(po_words)
    se2 = pd.Series(po_sentence)
    se3 = pd.Series(ne_words)
    se4 = pd.Series(ne_sentence)

    df['po_most_words'] = se1
    df['po_sentence'] = se2
    df['ne_most_words'] = se3
    df['ne_sentence'] = se4
    if not os.path.exists('c:/data/extract_.csv'):
        df.to_csv('c:/data/extract_.csv', index=False, mode='w', encoding='utf_8_sig')
    else:
        df.to_csv('c:/data/extract_.csv', index=False, mode='a', encoding='utf_8_sig', header=False)
    return df





