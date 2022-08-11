# -----------------------
import sys
# sys.path.append('./src') # pass
sys.path.append('../') # pass
import scraping_today as st
import pre_today as pt
import hr_macine_learning_today as ma
import get_info_scraping as gis
import send_email_today as set
import misc as misc
# -----------------------
from re import S
import datetime
import schedule
import time
import param
# -----------------------

# ----------------------------------------
# 今日のスケジュール情報を取得
# ----------------------------------------
def get_todays_sched():
    # --------------------------------
    date = datetime.datetime.now()    # 時間の取得
    y = str(date.year)                # 年
    # --------------------------------
    print(" start : getting {} / {}'s id".format(date.month, date.day))

    mode    = param.param()[3]
    # test用
    if mode == 0:
        id_list, rn_list = gis.get_id()   # 検索用idの取得
    elif mode == 1:
        id_list, rn_list = gis.get_id(param.param()[4])   # 検索用idの取得
    #end
    print(" end : getting {} / {}'s id".format(date.month, date.day))
    
    # id_list = [["新潟","2","3"], ["小倉","1","3"], ["中京","2","4"]]
    # rn_list = [[1,2,3...], [1,2,3...], [1,2,3...]]
    print(id_list)
    
    # c = ['020110','020110','020110']      # "競馬場id m日 n回目"
    c = []
    for i in range(len(id_list[0])):
        p = misc.conv_place_to_num(id_list[i][0]) # 場所を数字に変換
        c.append(str(p).zfill(2) + \
                 str(id_list[i][1]).zfill(2) + \
                 str(id_list[i][2]).zfill(2))
    #end
    # --------------------------------
    # --------------------------------
    print(" -------------- ")
    print(" Start Time of analysis ")
    print(" -------------- ")
    time_bf = param.param()[0]
    for i in range(len(c)):
        for j in rn_list[i]:
            id = y + c[i] + str(j).zfill(2)   # raceID,  "2022030204"
            stime = gis.only_get_time(id)     # start time, "10:50"

            h    = int(stime[0:2])            # hour
            m    = int(stime[3:5])            # min
            if m < time_bf:                   # x min 前に処理
                h = h - 1
                m = m - time_bf + 60
            else:
                m = m - time_bf
            #end
            m = str(int(m)).zfill(2)
            h = str(int(h)).zfill(2)
            bf15 = h + ":" + m                # 予測時刻
            print(bf15)
            
            # スケジュールの確保
            schedule.every().day.at(bf15).do(predict_keiba, id)
            
            # test用
            if mode == 1:
                schedule.every(2).seconds.do(predict_keiba, id)
                break
            #end
        #end

        # test用
        if mode == 1:
            break
        #end
    #end
    
    # test用
    if mode == 1:
        return schedule.CancelJob
    #end
#end

# ----------------------------------------
# 予測開始
# ----------------------------------------
def predict_keiba(id):
    print(" -------------- ")
    print(" Start analysis ")
    print(" -------------- ")

    dir = "model/"
    model_name = param.param()[1]
    # --------------------------------
    # --------------------------------
    # dt_now : データ取得時刻"20202020202_2008989832_today"
    # dname  : データ格納フォルダ名
    # e      : エラーか否か( e=0 : safe, e=1 : error )
    print(" start : scraping today's info ")
    dt_now, dname, Hassou_Time, e = st.scraping_today_info(id) 
    print(" end : scraping today's info ")
    
    if e == 0:
        print(" start : pre ")
        pt.pre(dname)                               # pre処理
        print(" end : pre ")
        print(" start : predict ")
        ma.macine_learning(dir + model_name, dname) # 機械学習
        print(" end : predict ")
    else:
        print("---------------\n")
        print(" Error at scraping !!!!!!!!!!!!")
        print("---------------\n")
    #end
    
    # e-mail
    print(" start : sending e-mail ")
    place = misc.conv_num_to_place(id[0:2])     # 場所を漢字に変換
    set.send_email(dt_now, place, id[-2:0], dname, Hassou_Time, e) # メールの送信
    print(" end : sending e-mail ")
    
    print("----------------------------------------\n")
    return schedule.CancelJob
#end