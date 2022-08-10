# --------------------------------
# --------------------------------
from re import S
# import to_day_py.scraping_today as st
# import to_day_py.pre_today as pt
# import to_day_py.hr_macine_learning_today as ma
import scraping_today as st
import pre_today as pt
import hr_macine_learning_today as ma
import get_info_scraping as gis
import send_email_today as set
# --------------------------------
# --------------------------------
import time
import datetime
import schedule
import time


def get_todays_sched(day):
    # --------------------------------
    date = datetime.datetime.now()
    y = str(date.year)
    # --------------------------------
    
    # ここを毎週変更すること !!!!!!!!!!!!!!!!!!!!!!!!!!
    
    """
    01 札幌 競馬場（北海道札幌市中央区）
    02 函館 競馬場（北海道函館市）
    03 福島 競馬場（福島県福島市）
    04 新潟 競馬場（新潟県新潟市北区）
    05 東京 競馬場（東京都府中市）
    06 中山 競馬場（千葉県船橋市・市川市）
    07 中京 競馬場（愛知県豊明市）
    08 京都 競馬場（京都府京都市伏見区）
    09 阪神 競馬場（兵庫県宝塚市・西宮市）
    10 小倉 競馬場（福岡県北九州市小倉南区）
    """
    

    # CODE = ['030204','100304','020110'] # 競馬場id and num
    if day == "Saturday":
    
        c = ['020110','020110','020110']      # 競馬場id n日 l回目
        rn = [9, 11]      # [ start, end ] number of race
    
    elif day == "Sunday":
    
        CODE = ['020110',] # 競馬場id and num
        RACE_NUM = ['09','10','11'] # 12 race
    
    #end



    # --------------------------------
    # レースナンバーの作成
    race_num = []
    ite = int(rn[1] - rn[0]) + 1
    for i in range(ite):
        race_num.append(str(rn + i).zfill(2))
    #end
    # --------------------------------
    for i in c:
        for j in race_num:
            id = y + i + j
            stime = gis.only_get_time(id) # raceID, ex) "2022030204"

            # stime = "10:10"
            h    = int(stime[0,2])  # hour
            m    = int(stime[3,5])  # min
            if m < 15:
                h = h - 1
                m = m - 15 + 60
            else:
                m = m - 15
            #end
            m = str(int(m)).zfill(2)
            h = str(int(h)).zfill(2)
            bf15 = h + ":" + m
            schedule.every().day.at(bf15).do(predict_keiba, id)
        #end
    #end
    # --------------------------------
#end

def predict_keiba(id):
    # --------------------------------
    # input
    # --------------------------------
    
    # model_name = 'RandomForest_2021.sav'
    # model_name = 'neural_network_2021.sav'
    model_name = 'lightgbm_2021.sav'

    # --------------------------------
    # --------------------------------
    dir = "model/"
    dt_now = st.main(id)
    pt.main()
    ma.main(dir + model_name)
    # e-mail
    place = conv_num_to_place(id[0:2])
    set.main(dt_now, place, id[-2:0])
    return schedule.CancelJob
#end

def main():
    # 毎週土日に08:00にその日のスケジュールを取得
    schedule.every().saturday.at("08:00").do(get_todays_sched, "Saturday")
    schedule.every().sunday.at("08:00").do(get_todays_sched, "Sunday")
    
    # 1秒毎にスケジュールを確認し、時間が来たら実行
    while True:
        schedule.run_pending()
        time.sleep(1)
    #end
#end

def conv_num_to_place(n):
    n = int(n)
    ret = ""
    if n == 1:
        ret = "札幌"
    elif n == 2:
        ret = "函館"
    elif n == 3:
        ret = "福島"
    elif n == 4:
        ret = "新潟"
    elif n == 5:
        ret = "東京"
    elif n == 6:
        ret = "中山"
    elif n == 7:
        ret = "中京"
    elif n == 8:
        ret = "京都"
    elif n == 9:
        ret = "阪神"
    elif n == 10:
        ret = "小倉"
    #end
    return ret
#end

# -----------------------------------
# -----------------------------------
main()