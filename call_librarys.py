
import call_url # url list 받아오기
import call_all_company

stopwords = ['도', '는', '다', '의', '가', '이', '은', '한', '에', '하', '고', '을', '를', '인', '듯', '과', '와', '네', '들', '듯', '지',
             '임', '게']


def classified_all_data():  # 분류된 전체 데이터
    url_dict = call_url.call_url()  # url리턴 함수
    load = call_all_company.weekly_all_classified_data(url_dict)
    return load

def none_classified_all_data(): #분류되지 않은 전체데이터
    url_dict= call_url.call_url() #url리턴 함수
    load= call_all_company.weekly_all_unclassified_data(url_dict)
    return load

def classified_selected_data(): #분류된 선택 데이터
    url,company= call_url.select_url() #url리턴 함수
    load= call_all_company.weekly_selected_classified_data(url, company)
    return load


def none_classified_selected_data():    #분류되지 않은 선택 데이터
    url,company= call_url.select_url()   #url리턴함수
    load= call_all_company.weekly_selected_unclassified_data(url, company)
    return load