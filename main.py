import import_ipynb

import important_sentence_output
import send_email
import call_librarys
import call_Graph
import pandas as pd
## 조건문 수정
#그래프 받고 안받고

def kwandoll():
    check1 = int(input("어떤 작업을 수행하시겠습니까?\n" + "[1]:경쟁회사 전체 데이터\n" + "[2]:경쟁회사 및 자사 데이터"))
    check2 = int(input("분류된 데이터를 확인하시겠습니까?\n" + "[1]:예" + "[2]:아니오"))
    check3 = int(input("이메일로 받으시겠습니까?\n" + "[1]:예" + "[2]:아니오"))
    check4 = int(input("그래프로 확인해보시겠습니까?\n" + "[1]:예" + "[2]:아니오"))
    if (check1 == 1):
        #경쟁회사 전체데이터 선택.
        if (check2 == 1 and check4 == 1):
            #분류된 데이터 그리고 그래프 확인

            call_librarys.classified_all_data()
            cloud_for_df = pd.read_csv("C:\\Data\\thisweek_classified.csv")
            negative,positive=important_sentence_output.output_sentence_all(cloud_for_df)
            data_frame=important_sentence_output.classifying(cloud_for_df)
            check5=int(input("어떤 시각화 자료를 보시겠습니까?\n"+
                             "[1]:긍,부정 빈도 그래프"+"[2]:긍,부정 문장"+"[3]:워드클라우드"))
            if(check5==1):
                #긍,부정 빈도그래프
                call_Graph.bar_plot(positive,negative)
            elif(check5==2):
                #긍,부정 문장
                print(data_frame)
                print("자료는 저장되었습니다.")
            elif(check5==3):
                #워드클라우드
                call_Graph.wordcloud(cloud_for_df)

            if (check3 == 1):
            #이메일 전송
                send_email.sending_classified_all_data()
            elif(check3==2):
            #이메일 미전송
                print("지정된 디렉토리에 저장되었습니다.")
        elif (check2 == 1 and check4 == 2):
            #분류된 데이터 그리고 그래프 미확인
            call_librarys.classified_all_data()
            if (check3 == 1):
            #이메일 전송
                send_email.sending_classified_all_data()
            elif(check3==2):
                print("지정된 디렉토리에 저장되었습니다.")
        elif (check2 == 2 and check4 == 1):
            #분류되지 않은 데이터 그리고 그래프 확인
            call_librarys.none_classified_all_data()
            cloud_for_df = pd.read_csv("C:\\Data\\thisweek_unclassified.csv")
            negative, positive = important_sentence_output.output_sentence_all(cloud_for_df)
            data_frame = important_sentence_output.classifying(cloud_for_df)
            check5 = int(input("어떤 시각화 자료를 보시겠습니까?\n" +
                               "[1]:긍,부정 빈도 그래프" + "[2]:긍,부정 문장" + "[3]:워드클라우드"))
            if (check5 == 1):
                # 긍,부정 빈도그래프
                call_Graph.bar_plot(positive, negative)

            elif (check5 == 2):
                # 긍,부정 문장
                print(data_frame)
                print("자료는 저장되었습니다.")
            elif (check5 == 3):
                # 워드클라우드
                call_Graph.wordcloud(cloud_for_df)
            if (check3 == 1):
            #이메일 전송
                send_email.sending_unclassified_all_data()
            elif(check3==2):
                print("지정된 디렉터리에 저장되었습니다.")
        elif (check2 == 2 and check4 == 2):
        #분류되지 않은 데이터 그리고 그래프 미확인
            call_librarys.none_classified_all_data()
            if (check3 == 1):
            #이메일 전송
                send_email.sending_unclassified_all_data()
            elif(check3==2):
            #이메일 미전송
                print("지정된 디렉토리에 저장되었습니다.")

    elif (check1 == 2):
    #경쟁회사 및 자사데이터
        if (check2 == 1 and check4 == 1):
        #분류된 데이터 그리고 그래프 확인
            call_librarys.classified_selected_data()
            cloud_for_df = pd.read_csv("C:\\Data\\thisweek_selected_classified.csv")
            negative, positive = important_sentence_output.output_sentence_all(cloud_for_df)
            data_frame = important_sentence_output.classifying(cloud_for_df)
            check5 = int(input("어떤 시각화 자료를 보시겠습니까?\n" +
                               "[1]:긍,부정 빈도 그래프" + "[2]:긍,부정 문장" + "[3]:워드클라우드"))
            if (check5 == 1):
                # 긍,부정 빈도그래프
                call_Graph.bar_plot(positive,negative)
            elif (check5 == 2):
                # 긍,부정 문장
                print(data_frame)
                print("자료는 저장되었습니다.")
            elif (check5 == 3):
                # 워드클라우드
                call_Graph.wordcloud(cloud_for_df)
            if (check3 == 1):
            #이메일 전송
                send_email.sending_classified_selected_data()
            elif(check3==2):
            #이메일 미전송
                print("지정된 디렉토리에 저장되었습니다.")
        elif (check2 == 1 and check4 == 2):
        #분류된 데이터 그리고 그래프 미확인
            call_librarys.classified_selected_data()
            if (check3 == 1):
            #이메일 전송
                send_email.sending_classified_selected_data()
            elif(check3==2):
            #이메일 미전송
                print("지정된 디렉토리에 저장되었습니다.")
        elif (check2 == 2 and check4 == 1):
        #분류되지 않은 데이터 그리고 그래프 확인
            call_librarys.none_classified_selected_data()
            cloud_for_df = pd.read_csv("C:\\Data\\thisweek_selected_unclassified.csv")
            negative, positive = important_sentence_output.output_sentence_all(cloud_for_df)
            data_frame = important_sentence_output.classifying(cloud_for_df)
            check5 = int(input("어떤 시각화 자료를 보시겠습니까?\n" +
                               "[1]:긍,부정 빈도 그래프" + "[2]:긍,부정 문장" + "[3]:워드클라우드"))
            if (check5 == 1):
                # 긍,부정 빈도그래프
                call_Graph.bar_plot(positive,negative)

            elif (check5 == 2):
                # 긍,부정 문장
                print(data_frame)
                print("자료는 저장되었습니다.")
            elif (check5 == 3):
                # 워드클라우드
                call_Graph.wordcloud(cloud_for_df)

            if (check3 == 1):
            #이메일 전송
                send_email.sending_unclassified_selected_data()
            elif(check3==2):
            #이메일 미전송
                print("지정된 디렉토리에 저장되었습니다.")
        elif (check2 == 2 and check4 == 2):
        #분류되지 않은 데이터 그리고 그래프 미확인
            call_librarys.none_classified_selected_data()  #change1
            if (check3 == 1):
            #이메일 전송
                send_email.sending_unclassified_selected_data()
            elif(check3==2):
            #이메일 미전송
                print("지정된 디렉토리에 저장되었습니다.")



kwandoll()

