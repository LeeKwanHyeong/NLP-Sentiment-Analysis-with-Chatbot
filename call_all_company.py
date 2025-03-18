
#sklearn

#konlpy
from konlpy.tag import Okt
import call_GRU_predict
import pandas as pd
import numpy as np

import re
import os
import time, datetime

from datetime import datetime,timedelta
import pyautogui
#Crawling
from bs4 import BeautifulSoup
from selenium import webdriver

from selenium.webdriver.chrome.options import Options
options=Options()
options.add_argument('--start-fullscreen')



stopwords = ['도', '는', '다', '의', '가', '이', '은', '한', '에', '하', '고', '을', '를', '인', '듯', '과', '와', '네', '들', '듯', '지', '임', '게']


def start_to_date():
    start_date_list = []
    st = input("시작 년도를 적으시오: ")
    start_date_list.append(st)
    st = input("시작 월을 적으시오: ")
    start_date_list.append(st)
    st = input("시작 일을 적으시오: ")
    start_date_list.append(st)
    s_year, s_month, s_day = int(start_date_list[0]), int(start_date_list[1]), int(start_date_list[2])
    start_date = datetime(s_year, s_month, s_day)
    return start_date


def end_to_date():
    end_date_list = []
    et = input("종료 년도를 적으시오: ")
    end_date_list.append(et)
    et = input("종료 월을 적으시오: ")
    end_date_list.append(et)
    et = input("종료 일을 적으시오: ")
    end_date_list.append(et)
    e_year, e_month, e_day = int(end_date_list[0]), int(end_date_list[1]), int(end_date_list[2])
    end_date = datetime(e_year, e_month, e_day)

    return end_date

def score_input():
    maximum_score=int(input("Semantic Value 의 Maximum 값을 지정하세요: "))
    minimum_score=int(input("Semantic Value 의 Minumum 값을 지정하세요: "))
    maximum_score,minimum_score=float(maximum_score),float(minimum_score)
    return maximum_score,minimum_score

def weekly_all_classified_data(dict):
    start_date, end_date = start_to_date(), end_to_date()
    maximum, minimum = score_input()
    for key, value in dict.items():
        driver = webdriver.Chrome('C:\\Users\\LeeKwanHyeong\\chromedriver_win32\\chromedriver.exe',
                                  chrome_options=options) #change1
        driver.implicitly_wait(2)
        driver.get(value)
        # sort 선택창
        elem = driver.find_element_by_xpath("//span[@class='DPvwYc']")
        elem.click()
        time.sleep(3)
        pyautogui.press('up')
        time.sleep(0.7)
        pyautogui.press('up')
        time.sleep(0.7)
        pyautogui.press('enter')

        while (True):
            driver.execute_script("window.scrollTo([0],document.body.scrollHeight);")
            time.sleep(0.5)
            try:
                element = driver.find_element_by_xpath('//div[@class="U26fgb O0WRkf oG5Srb C0oVfc n9lfJ"]')
                if (element is not None):
                    element.click()
                    break
            except Exception:
                continue

        html = driver.page_source
        driver.quit()
        bsObj = BeautifulSoup(html, 'lxml')
        div_reviews = bsObj.find_all("div", {"class": "d15Mdf bAhLNe"})

        company_list, grade_list, date_list, content_list = [], [], [], []
        for div in div_reviews:

            date_ = div.find('span', {"class": "p2TkOb"}).get_text()
            t = re.findall(r"\d*\.\d+|\d+", date_)
            date = '{0}-{1}-{2}'.format(t[0], t[1], t[2])
            year, month, day = int(t[0]), int(t[1]), int(t[2])
            dd = datetime(year, month, day)
            if ((dd - start_date >= timedelta(days=0)) and (end_date - dd >= timedelta(days=0))):
                content = div.find('span', {'jsname': 'bN97Pc'}).get_text()
                content = content.replace("전체 리뷰", '')
                content = re.sub('[^가-힣0-9a-zA-Z_!?@#%^&-=:;,\"\'<>\\s]', '', content)
                content.encode('utf-8')
                grade = len(div.find_all('div', {'class': 'vQHuPe bUWb7c'}))
                percentage, word = call_GRU_predict.GRU_predict(content)
                if (((percentage < maximum) and (percentage > minimum))) and (len(word) > 6):
                    date_list.append(dd)
                    content_list.append(content)
                    grade_list.append(grade)
                    company_list.append(key)
                else:
                    continue
        grade_Series = pd.Series(grade_list)
        date_Series = pd.Series(date_list)
        content_Series = pd.Series(content_list)
        #
        company_Series = pd.Series(company_list)
        data_frame = pd.DataFrame()
        data_frame['company'] = company_Series
        data_frame['date'] = date_Series
        data_frame['grade'] = grade_Series
        data_frame['content'] = content_Series



        if not os.path.exists('C:\\Data\\thisweek_classified.csv'): #change2
            data_frame.to_csv('C:\\Data\\thisweek_classified.csv', index=False, mode='w', encoding='utf_8_sig') #change2
        else:
            data_frame.to_csv('C:\\Data\\thisweek_classified.csv', index=False, mode='a', encoding='utf_8_sig', #change2
                              header=False)
    xlsx=pd.read_csv('C:/Data/thisweek_classified.csv')#change 2
    xlsx=pd.DataFrame(xlsx)
    good_data=xlsx[xlsx['grade']>2]
    bad_data=xlsx[xlsx['grade']<3]
    writer=pd.ExcelWriter("C:/data/thisweek_classified.xlsx")#change2
    good_data.to_excel(writer,sheet_name='good',header=True)
    bad_data.to_excel(writer,sheet_name='bad',header=True)
    writer.save()
    return data_frame

    # location='C:\\Data\\thisweek_classified.csv'
def weekly_all_unclassified_data(dict):
    start_date, end_date = start_to_date(), end_to_date()
    for key, value in dict.items():
        driver = webdriver.Chrome('C:\\Users\\LeeKwanHyeong\\chromedriver_win32\\chromedriver.exe', #change1
                                  chrome_options=options)
        driver.implicitly_wait(2)
        driver.get(value)
        # sort 선택창
        elem = driver.find_element_by_xpath("//span[@class='DPvwYc']")
        elem.click()
        time.sleep(3)
        pyautogui.press('up')
        time.sleep(0.7)
        pyautogui.press('up')
        time.sleep(0.7)
        pyautogui.press('enter')

        while (True):
            driver.execute_script("window.scrollTo([0],document.body.scrollHeight);")
            time.sleep(0.5)
            try:
                element = driver.find_element_by_xpath('//div[@class="U26fgb O0WRkf oG5Srb C0oVfc n9lfJ"]')
                if (element is not None):
                    element.click()
                    break
            except Exception:
                continue

        html = driver.page_source
        driver.quit()
        bsObj = BeautifulSoup(html, 'lxml')
        div_reviews = bsObj.find_all("div", {"class": "d15Mdf bAhLNe"})

        company_list, grade_list, date_list, content_list = [], [], [], []
        for div in div_reviews:

            date_ = div.find('span', {"class": "p2TkOb"}).get_text()
            t = re.findall(r"\d*\.\d+|\d+", date_)
            date = '{0}-{1}-{2}'.format(t[0], t[1], t[2])
            year, month, day = int(t[0]), int(t[1]), int(t[2])
            dd = datetime(year, month, day)
            if ((dd - start_date >= timedelta(days=0)) and (end_date - dd >= timedelta(days=0))):
                content = div.find('span', {'jsname': 'bN97Pc'}).get_text()
                content = content.replace("전체 리뷰", '')
                content = re.sub('[^가-힣0-9a-zA-Z_!?@#%^&-=:;,\"\'<>\\s]', '', content)
                content.encode('utf-8')
                grade = len(div.find_all('div', {'class': 'vQHuPe bUWb7c'}))
                percentage, word = call_GRU_predict.GRU_predict(content)

                date_list.append(dd)
                content_list.append(content)
                grade_list.append(grade)
                company_list.append(key)

                grade_Series = pd.Series(grade_list)
                date_Series = pd.Series(date_list)
                content_Series = pd.Series(content_list)
                #
                company_Series = pd.Series(company_list)
                data_frame = pd.DataFrame()
                data_frame['company'] = company_Series
                data_frame['date'] = date_Series
                data_frame['grade'] = grade_Series
                data_frame['content'] = content_Series


        if not os.path.exists('C:\\Data\\thisweek_unclassified.csv'):#change2
            data_frame.to_csv('C:\\Data\\thisweek_unclassified.csv', index=False, mode='w', encoding='utf_8_sig')
        else:#change2
            data_frame.to_csv('C:\\Data\\thisweek_unclassified.csv', index=False, mode='a', encoding='utf_8_sig',
                          header=False)#change2
    xlsx = pd.read_csv('C:/Data/thisweek_classified.csv')  # change 2
    xlsx = pd.DataFrame(xlsx)
    good_data = xlsx[xlsx['grade'] > 2]
    bad_data = xlsx[xlsx['grade'] < 3]
    writer = pd.ExcelWriter("C:/data/thisweek_classified.xlsx")  # change2
    good_data.to_excel(writer, sheet_name='good', header=True)
    bad_data.to_excel(writer, sheet_name='bad', header=True)
    writer.save()
    # all_data=pd.read_csv("C:\\Data\\thisweek_unclassified.csv")
    return data_frame
def weekly_selected_classified_data(url, company):
    start_date, end_date = start_to_date(), end_to_date()
    maximum, minimum = score_input()

    driver = webdriver.Chrome('C:\\Users\\LeeKwanHyeong\\chromedriver_win32\\chromedriver.exe', chrome_options=options)#change1
    driver.implicitly_wait(2)
    driver.get(url)
    # sort 선택창
    elem = driver.find_element_by_xpath("//span[@class='DPvwYc']")
    elem.click()
    time.sleep(3)
    pyautogui.press('up')
    time.sleep(0.7)
    pyautogui.press('up')
    time.sleep(0.7)
    pyautogui.press('enter')

    while (True):
        driver.execute_script("window.scrollTo([0],document.body.scrollHeight);")
        time.sleep(0.5)
        try:
            element = driver.find_element_by_xpath('//div[@class="U26fgb O0WRkf oG5Srb C0oVfc n9lfJ"]')
            if (element is not None):
                element.click()
                break
        except Exception:
            continue
    html = driver.page_source
    driver.quit()
    bsObj = BeautifulSoup(html, 'lxml')
    div_reviews = bsObj.find_all("div", {"class": "d15Mdf bAhLNe"})

    #
    company_list, grade_list, date_list, content_list = [], [], [], []

    for div in div_reviews:
        date_ = div.find('span', {"class": "p2TkOb"}).get_text()
        t = re.findall(r"\d*\.\d+|\d+", date_)
        date = '{0}-{1}-{2}'.format(t[0], t[1], t[2])
        year, month, day = int(t[0]), int(t[1]), int(t[2])
        dd = datetime(year, month, day)
        if ((dd - start_date >= timedelta(days=0)) and (end_date - dd >= timedelta(days=0))):
            content = div.find('span', {'jsname': 'bN97Pc'}).get_text()
            content = content.replace("전체 리뷰", '')
            content = re.sub('[^가-힣0-9a-zA-Z_!?@#%^&-=:;,\"\'<>\\s]', '', content)
            content.encode('utf-8')
            grade = len(div.find_all('div', {'class': 'vQHuPe bUWb7c'}))
            percentage, word = call_GRU_predict.GRU_predict(content)
            if (((percentage < maximum) and (percentage > minimum))) and (len(word) > 6):
                date_list.append(dd)
                content_list.append(content)
                grade_list.append(grade)
                company_list.append(company)
            else:
                continue
    grade_Series = pd.Series(grade_list)
    date_Series = pd.Series(date_list)
    content_Series = pd.Series(content_list)
    #
    company_Series = pd.Series(company_list)
    data_frame = pd.DataFrame()
    data_frame['company'] = company_Series
    data_frame['date'] = date_Series
    data_frame['grade'] = grade_Series
    data_frame['content'] = content_Series
    #
    good_data = data_frame[data_frame['grade'] > 2]
    bad_data = data_frame[data_frame['grade'] < 3]
    if not os.path.exists('C:\\Data\\thisweek_selected_classified.csv'): #change2
        data_frame.to_csv('C:\\Data\\thisweek_selected_classified.csv', index=False, mode='w', encoding='utf_8_sig')
    else:#change2
        data_frame.to_csv('C:\\Data\\thisweek_selected_classified.csv', index=False, mode='a', encoding='utf_8_sig',
                          header=False)#change2

    writer = pd.ExcelWriter('C:/data/thisweek_selected_classified.xlsx')#change2
    if not os.path.exists(writer):
        good_data.to_excel(writer, sheet_name='good', header=True)
        bad_data.to_excel(writer, sheet_name='bad', header=True)
    else:
        good_data.to_excel(writer, sheet_name='good', header=False)
        bad_data.to_excel(writer, sheet_name='bad', header=False)
    writer.save()
    return data_frame
def weekly_selected_unclassified_data(url, company):
    start_date, end_date = start_to_date(), end_to_date()
    driver = webdriver.Chrome('C:\\Users\\LeeKwanHyeong\\chromedriver_win32\\chromedriver.exe', chrome_options=options) #change1
    driver.implicitly_wait(2)
    driver.get(url)
    # sort 선택창
    elem = driver.find_element_by_xpath("//span[@class='DPvwYc']")
    elem.click()
    time.sleep(3)
    pyautogui.press('up')
    time.sleep(0.7)
    pyautogui.press('up')
    time.sleep(0.7)
    pyautogui.press('enter')

    while (True):
        driver.execute_script("window.scrollTo([0],document.body.scrollHeight);")
        time.sleep(0.5)
        try:
            element = driver.find_element_by_xpath('//div[@class="U26fgb O0WRkf oG5Srb C0oVfc n9lfJ"]')
            if (element is not None):
                element.click()
                break
        except Exception:
            continue
    html = driver.page_source
    driver.quit()
    bsObj = BeautifulSoup(html, 'lxml')
    div_reviews = bsObj.find_all("div", {"class": "d15Mdf bAhLNe"})

    #
    company_list, grade_list, date_list, content_list = [], [], [], []

    for div in div_reviews:
        date_ = div.find('span', {"class": "p2TkOb"}).get_text()
        t = re.findall(r"\d*\.\d+|\d+", date_)
        date = '{0}-{1}-{2}'.format(t[0], t[1], t[2])
        year, month, day = int(t[0]), int(t[1]), int(t[2])
        dd = datetime(year, month, day)
        if ((dd - start_date >= timedelta(days=0)) and (end_date - dd >= timedelta(days=0))):
            content = div.find('span', {'jsname': 'bN97Pc'}).get_text()
            content = content.replace("전체 리뷰", '')
            content = re.sub('[^가-힣0-9a-zA-Z_!?@#%^&-=:;,\"\'<>\\s]', '', content)
            content.encode('utf-8')
            grade = len(div.find_all('div', {'class': 'vQHuPe bUWb7c'}))
            percentage, word = call_GRU_predict.GRU_predict(content)

            date_list.append(dd)
            content_list.append(content)
            grade_list.append(grade)
            company_list.append(company)
    grade_Series = pd.Series(grade_list)
    date_Series = pd.Series(date_list)
    content_Series = pd.Series(content_list)
    #
    company_Series = pd.Series(company_list)
    data_frame = pd.DataFrame()
    data_frame['company'] = company_Series
    data_frame['date'] = date_Series
    data_frame['grade'] = grade_Series
    data_frame['content'] = content_Series
    #
    good_data = data_frame[data_frame['grade'] > 2]
    bad_data = data_frame[data_frame['grade'] > 3]

    writer = pd.ExcelWriter("C:/data/thisweek_selected_unclassified.xlsx") #change2
    if not os.path.exists(writer):
        good_data.to_excel(writer, sheet_name='good', header=True)
        bad_data.to_excel(writer, sheet_name='bad', header=True)
    else:

        good_data.to_excel(writer, sheet_name='good', header=False)
        bad_data.to_excel(writer, sheet_name='bad', header=False)
    writer.save()
    if not os.path.exists('C:\\Data\\thisweek_selected_unclassified.csv'): #change2
        data_frame.to_csv('C:\\Data\\thisweek_selected_unclassified.csv', index=False, mode='w', encoding='utf_8_sig')
    else:#change2
        data_frame.to_csv('C:\\Data\\thisweek_selected_unclassified.csv', index=False, mode='a', encoding='utf_8_sig',
                          header=False)#change2

    return data_frame


