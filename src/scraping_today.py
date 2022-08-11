# ------------------------------------
# horse_racing
# ------------------------------------

# ------------------------------------
# スクレイピングに必要なモジュール
# ------------------------------------
import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import pandas as pd
from tqdm import tqdm

# ------------------------------------
# import
# ------------------------------------
import time
import sys
import re
import numpy
import pandas as pd
import itertools
import os
import shutil
import datetime

# ------------------------------------
# main
# ------------------------------------
def scraping_today_info(id):
    
    # サイトURLの作成
    sitename = "https://race.netkeiba.com/race/shutuba.html?race_id={}".format(id)

    # ------------------------------------
    # mkdir
    # ------------------------------------
    dt_now = datetime.datetime.now()
    dname = dt_now.strftime('%Y%m%d%H%M%S') + "_" + id + "_today"
    os.makedirs(dname, exist_ok=True)
    
    # ------------------------------------
    # ------------------------------------
    ite = 0
    result_df = pd.DataFrame()            # データ格納用
    start = time.time()
    # ------------------------------------
    # ------------------------------------
    # スクレイピング対象の URL にリクエストを送り HTML を取得する
    res = requests.get(sitename)
    res.raise_for_status()  #URLが正しくない場合，例外を発生させる

    # 時間をあけてアクセスするように、sleepを設定する
    time.sleep(1.1)
    
    # レスポンスの HTML から BeautifulSoup オブジェクトを作る
    soup = BeautifulSoup(res.content, 'html.parser')
    
    # 動的用セッション開始
    session = HTMLSession()
    r = session.get(sitename)
    # ブラウザエンジンでHTMLを生成させる
    r.html.render(timeout=60)

    # ------------------------------------
    # ------------------------------------
    e = 0 # errorか否か
    try:
        # ------------------------------------
        # 棄権等の確認
        # ------------------------------------
        kiken_list = []
        span = r.html.find('span')            # "span"内のデータ取得
        
        for i in range(18):                   # 最大馬数
            kiken = []
            for l in span:
                ll = l.find('#ninki-1_' + str(i+1).zfill(2)) # 馬番号で検索
                if ll != []:                                 
                    kiken.append(ll)
                #end
            #end
            
            if len(kiken) > 0:
                pass
            else:
                kiken_list.append(i)                         # 棄権の番号を格納
            #end
        #end

        # ------------------------------------
        #順位のリスト作成
        # ------------------------------------
        # Ranks = soup.find_all('div', class_='Rank')
        # Ranks_list = []
        # for Rank in Ranks:
        #     Rank = Rank.get_text()
        #     #リスト作成
        #     Ranks_list.append(Rank)
        # #end
        
        # ------------------------------------
        #馬名取得
        # ------------------------------------
        Horse_Names = soup.find_all('span', class_='HorseName')
        Horse_Names_list = []
        for Horse_Name in Horse_Names[1:]:
            #馬名のみ取得(lstrip()先頭の空白削除，rstrip()改行削除)
            Horse_Name = Horse_Name.get_text().lstrip().rstrip('\n')
            #リスト作成
            Horse_Names_list.append(Horse_Name)
        #end

        # ------------------------------------
        #騎手名取得
        # ------------------------------------
        Trainers = soup.find_all('td', class_='Trainer')
        Trainers_list = []
        for Trainer in Trainers:
            #馬名のみ取得(lstrip()先頭の空白削除，rstrip()改行削除)
            Trainer = Trainer.get_text().lstrip().rstrip('\n')
            #リスト作成
            Trainers_list.append(Trainer)
        #end

        # ------------------------------------
        # 体重取得
        # ------------------------------------
        Weights = soup.find_all('td', class_='Weight')
        Weights_list = []
        for Weight in Weights:
            #馬名のみ取得(lstrip()先頭の空白削除，rstrip()改行削除)
            Weight = Weight.get_text().lstrip().rstrip('\n')
            #リスト作成
            Weights_list.append(Weight)
        #end

        # ------------------------------------
        # 性齢取得
        # ------------------------------------
        # Olds = soup.find_all('span', class_='Barei Txt_C')
        Olds = soup.find_all('td', class_='Barei Txt_C')
        Olds_list = []
        for Old in Olds:
            #馬名のみ取得(lstrip()先頭の空白削除，rstrip()改行削除)
            Old = Old.get_text().lstrip().rstrip('\n')
            #リスト作成
            Olds_list.append(Old)
        #end

        # ------------------------------------
        # 斤量取得
        # ------------------------------------
        # JockeyWeights = soup.find_all('span', class_='TxT_C')
        JockeyWeights = soup.find_all('td', class_='Txt_C')
        JockeyWeights_list = []
        for JockeyWeight in JockeyWeights:
            #馬名のみ取得(lstrip()先頭の空白削除，rstrip()改行削除)
            JockeyWeight = JockeyWeight.get_text().lstrip().rstrip('\n')
            if len(JockeyWeight) == 4:
                #リスト作成
                JockeyWeights_list.append(JockeyWeight)
            #end
        #end

        # ------------------------------------
        #人気取得
        # ------------------------------------       
        # Ninkis = soup.find_all('td', class_='Txt_R Popular')
        Ninkis_list = []

        td = r.html.find('.Popular')               # class="Popular"の検索
        for i in td:
            c = i.find('.Txt_C')                   # class="Popular TxT_C"の検索
            for j in c:
                cc = j.find('.Popular_Ninki')      # class="Popular TxT_C Popular_Ninki"の検索

                if cc != []:
                    # print(c[0].text)
                    Ninkis_list.append(cc[0].text) # 格納
                #end
            #end
        #end
        Ninkis_list = Ninkis_list[1:]
        
        # for Ninki in Ninkis:
        #     Ninki = Ninki.get_text()
        #     #リスト作成
        #     Ninkis_list.append(Ninki)
        # #end

        # ------------------------------------
        #オッズ取得
        # ------------------------------------
        # Odds_Ninkis = soup.find_all('td', class_='Odds Txt_R')
        Odds_Ninkis_list = []
        # ite_odds = 0
        # for Odds_Ninki in Odds_Ninkis:
        #     #Odds_Ninki = Odds_Ninki.get_text()
        #     Odds_Ninki = str(Odds_Ninkis[ite_odds])
        #     Odds_Ninki  = Odds_Ninki.replace("\n","")
        #     Odds_Ninki  = Odds_Ninki.replace("\"","")
        #     Odds_Ninki  = (Odds_Ninki.split(">")[2]).split("<")[0]
        #     #リスト作成
        #     Odds_Ninkis_list.append(Odds_Ninki)

        #     ite_odds +=1
        # #end
        
        td = r.html.find('.Popular')
        for i in td:
            c = i.find('.Txt_R')
            if c != []:
                # print(c[0].text)
                Odds_Ninkis_list.append(c[0].text)
            #end
        #end

        # ------------------------------------
        #コーナー通過
        # ------------------------------------
        # Orders = soup.find_all('td', class_='PassageRate')
        # Order_list = []
        # for Order in Orders:
        #     #馬名のみ取得(lstrip()先頭の空白削除，rstrip()改行削除)
        #     Order = Order.get_text().lstrip().rstrip('\n')
        #     #リスト作成
        #     Order_list.append(Order)
        # #end
        
        # ------------------------------------
        #枠取得
        # ------------------------------------
        # Wakus = soup.find_all('td', class_=re.compile("Num Waku"))
        Wakus = []
        for i in range(1, 16):
            Waku = soup.find_all('td', class_="Waku" +str(i)+" Txt_C")
            if Waku != []:
                for j in range(len(Waku)):
                    Wakus.append(Waku[j])
                #end
            #end
        #end
        
        Wakus_list = []
        for Waku in Wakus:
            Waku_ = Waku.get_text().lstrip().rstrip('\n')
            #リスト作成
            Wakus_list.append(Waku_)
        #end

        # ------------------------------------
        # 馬番取得
        # ------------------------------------
        horsenum_list = []
        for i in range(1, 16):
            horsenum = soup.find_all('td', class_="Umaban"+str(i)+" Txt_C")
            if horsenum != []:
                for j in range(len(horsenum)):
                    horsenum_list.append(horsenum[j])
                #end
            #end
        #end

        horsenums_list = []
        for horsenum in horsenum_list:
            horsenum_ = horsenum.get_text().lstrip().replace('\n','')
            #リスト作成
            horsenums_list.append(horsenum_)
        #end

        # ------------------------------------
        #コース,距離取得
        # ------------------------------------
        Distance_Course = soup.find_all('span')
        Distance_Course = re.search(r'.[0-9]+m', str(Distance_Course))
        Course = Distance_Course.group()[0]
        Distance = re.sub("\\D", "", Distance_Course.group())

        # ------------------------------------
        # 発走時刻，天気，馬場，
        # ------------------------------------
        RaceData01 = soup.find_all('div', class_='RaceData01')
        RaceData01 = str(RaceData01[0])
        RaceData01  = RaceData01.split("\n")
        
        """
        RaceData01 = ['<div class="RaceData01">',
                    '09:55発走 /<!-- <span class="Turf"> --><span> 芝1800m</span> (右)',
                    '/ 天候:曇<span class="Icon_Weather Weather02"></span>',
                    '<span class="Item03">/ 馬場:良</span>',
                    '</div>']
        """
        StartTime    = RaceData01[1].split("発走")[0]
        Weather      = (RaceData01[2].split("天候:")[1]).split("<")[0]
        RidingGround = (RaceData01[3].split("馬場:")[1]).split("<")[0]

        # ------------------------------------
        # 棄権等の調整
        # ------------------------------------
        # 棄権の箇所は0を格納
        if len(kiken_list) > 0:
            print(kiken_list)
            for i in range(len(kiken_list)):
                if kiken_list[i] < len(horsenum_list):
                    Weights_list.insert(kiken_list[i], '0')
                    Ninkis_list.insert(kiken_list[i], '0')
                    Odds_Ninkis_list.insert(kiken_list[i], '0')
                    Olds_list.insert(kiken_list[i], '0')

                    Horse_Names_list[kiken_list[i]] = '0'
                    Trainers_list[kiken_list[i]] = '0'
                    JockeyWeights_list[kiken_list[i]] = '0'
                #end
            #end
        #end
        
        # ------------------------------------
        # ------------------------------------
        n = len(Wakus_list)
        Ranks_list = [0] * n
        Order_list = [0] * n

        print("----------------")
        print(Ranks_list)
        print(Wakus_list)
        print(Horse_Names_list)
        print(Trainers_list)
        print(Weights_list)
        print(Olds_list)
        print(JockeyWeights_list)
        print(Course)
        print(Distance)
        print(Weather)
        print(RidingGround)
        print(Ninkis_list)
        print(Odds_Ninkis_list)
        print(Order_list)
        print(horsenums_list)
        print("----------------")
        # ------------------------------------
        # ------------------------------------
        df = pd.DataFrame({
            'レースID':''.join(id),
            '順位':Ranks_list,
            '枠':Wakus_list,
            '馬名':Horse_Names_list,
            '騎手名':Trainers_list,
            '体重':Weights_list,
            '年齢':Olds_list,
            '斤量':JockeyWeights_list,
            'コース':Course,
            '距離':Distance,
            '発走':StartTime,
            '天候':Weather,
            '馬場':RidingGround,
            '人気':Ninkis_list,
            'オッズ':Odds_Ninkis_list,
            'コーナー通過順':Order_list,
            '馬番':horsenums_list,
        })
        
        result_df = pd.concat([result_df,df],axis=0)

        # ------------------------------------
        # ------------------------------------
        # print(sys.exc_info())
        # print(race_id)
        # print("サイト取得エラー")
        
        # ------------------------------------
        # elapsed time
        # ------------------------------------
        ite += 1
        elapsed_time = time.time() - start
        print(str(len(id)) +  \
                " : {:.2f}".format(elapsed_time) + " s")
        
        # ------------------------------------
        # output
        # ------------------------------------
        if result_df.empty == False:
            f = dname + "\\" + id
            result_df.to_csv(f, encoding="utf-8")
        #end
    except:
        e = 1
    #end

    return dt_now.strftime('%Y%m%d%H%M%S'), dname, StartTime, e
#end

def main_copy(id):
    
    # サイトURLの作成
    sitename = "https://race.netkeiba.com/race/shutuba.html?race_id={}".format(id)

    # ------------------------------------
    # mkdir
    # ------------------------------------
    dt_now = datetime.datetime.now()
    dname = dt_now.strftime('%Y%m%d%H%M%S') + "_" + id + "_today"
    os.makedirs(dname, exist_ok=True)
    
    # ------------------------------------
    # ------------------------------------
    #サイトURLをループしてデータを取得する
    ite = 0
    result_df = pd.DataFrame()
    start = time.time()
    # ------------------------------------
    # ------------------------------------
    # スクレイピング対象の URL にリクエストを送り HTML を取得する
    res = requests.get(sitename)
    res.raise_for_status()  #URLが正しくない場合，例外を発生させる

    # 時間をあけてアクセスするように、sleepを設定する
    time.sleep(1.1)
    
    # レスポンスの HTML から BeautifulSoup オブジェクトを作る
    soup = BeautifulSoup(res.content, 'html.parser')
    
    # title タグの文字列を取得する
    title_text = soup.find('title').get_text()

    # 動的用セッション開始
    session = HTMLSession()
    r = session.get(sitename)
    # ブラウザエンジンでHTMLを生成させる
    r.html.render(timeout=60)
    
    
    e = 0 
    # ------------------------------------
    # 棄権等の確認
    # ------------------------------------
    kiken_list = []
    span = r.html.find('span')
    
    for i in range(18):
        kiken = []
        for l in span:
            ll = l.find('#ninki-1_' + str(i+1).zfill(2))
            if ll != []:
                kiken.append(ll)
            #end
        #end
        
        if len(kiken) > 0:
            pass
        else:
            kiken_list.append(i)
        #end
    #end

    # ------------------------------------
    #順位のリスト作成
    # ------------------------------------
    # Ranks = soup.find_all('div', class_='Rank')
    # Ranks_list = []
    # for Rank in Ranks:
    #     Rank = Rank.get_text()
    #     #リスト作成
    #     Ranks_list.append(Rank)
    # #end
    
    # ------------------------------------
    #馬名取得
    # ------------------------------------
    Horse_Names = soup.find_all('span', class_='HorseName')
    Horse_Names_list = []
    for Horse_Name in Horse_Names[1:]:
        #馬名のみ取得(lstrip()先頭の空白削除，rstrip()改行削除)
        Horse_Name = Horse_Name.get_text().lstrip().rstrip('\n')
        #リスト作成
        Horse_Names_list.append(Horse_Name)
    #end

    # ------------------------------------
    #騎手名取得
    # ------------------------------------
    Trainers = soup.find_all('td', class_='Trainer')
    Trainers_list = []
    for Trainer in Trainers:
        #馬名のみ取得(lstrip()先頭の空白削除，rstrip()改行削除)
        Trainer = Trainer.get_text().lstrip().rstrip('\n')
        #リスト作成
        Trainers_list.append(Trainer)
    #end

    # ------------------------------------
    # 体重取得
    # ------------------------------------
    Weights = soup.find_all('td', class_='Weight')
    Weights_list = []
    for Weight in Weights:
        #馬名のみ取得(lstrip()先頭の空白削除，rstrip()改行削除)
        Weight = Weight.get_text().lstrip().rstrip('\n')
        #リスト作成
        Weights_list.append(Weight)
    #end

    # ------------------------------------
    # 性齢取得
    # ------------------------------------
    # Olds = soup.find_all('span', class_='Barei Txt_C')
    Olds = soup.find_all('td', class_='Barei Txt_C')
    Olds_list = []
    for Old in Olds:
        #馬名のみ取得(lstrip()先頭の空白削除，rstrip()改行削除)
        Old = Old.get_text().lstrip().rstrip('\n')
        #リスト作成
        Olds_list.append(Old)
    #end

    # ------------------------------------
    # 斤量取得
    # ------------------------------------
    # JockeyWeights = soup.find_all('span', class_='TxT_C')
    JockeyWeights = soup.find_all('td', class_='Txt_C')
    JockeyWeights_list = []
    for JockeyWeight in JockeyWeights:
        #馬名のみ取得(lstrip()先頭の空白削除，rstrip()改行削除)
        JockeyWeight = JockeyWeight.get_text().lstrip().rstrip('\n')
        if len(JockeyWeight) == 4:
            #リスト作成
            JockeyWeights_list.append(JockeyWeight)
        #end
    #end

    # ------------------------------------
    #人気取得
    # ------------------------------------       
    # Ninkis = soup.find_all('td', class_='Txt_R Popular')
    Ninkis_list = []

    td = r.html.find('.Popular')
    for i in td:
        c = i.find('.Txt_C')
        for j in c:
            cc = j.find('.Popular_Ninki')

            if cc != []:
                # print(c[0].text)
                Ninkis_list.append(cc[0].text)
            #end
        #end
    #end
    Ninkis_list = Ninkis_list[1:]
    
    # for Ninki in Ninkis:
    #     Ninki = Ninki.get_text()
    #     #リスト作成
    #     Ninkis_list.append(Ninki)
    # #end

    # ------------------------------------
    #オッズ取得
    # ------------------------------------
    # Odds_Ninkis = soup.find_all('td', class_='Odds Txt_R')
    Odds_Ninkis_list = []
    # ite_odds = 0
    # for Odds_Ninki in Odds_Ninkis:
    #     #Odds_Ninki = Odds_Ninki.get_text()
    #     Odds_Ninki = str(Odds_Ninkis[ite_odds])
    #     Odds_Ninki  = Odds_Ninki.replace("\n","")
    #     Odds_Ninki  = Odds_Ninki.replace("\"","")
    #     Odds_Ninki  = (Odds_Ninki.split(">")[2]).split("<")[0]
    #     #リスト作成
    #     Odds_Ninkis_list.append(Odds_Ninki)

    #     ite_odds +=1
    # #end
    
    td = r.html.find('.Popular')
    for i in td:
        c = i.find('.Txt_R')
        if c != []:
            # print(c[0].text)
            Odds_Ninkis_list.append(c[0].text)
        #end
    #end

    # ------------------------------------
    #コーナー通過
    # ------------------------------------
    # Orders = soup.find_all('td', class_='PassageRate')
    # Order_list = []
    # for Order in Orders:
    #     #馬名のみ取得(lstrip()先頭の空白削除，rstrip()改行削除)
    #     Order = Order.get_text().lstrip().rstrip('\n')
    #     #リスト作成
    #     Order_list.append(Order)
    # #end
    
    # ------------------------------------
    #枠取得
    # ------------------------------------
    # Wakus = soup.find_all('td', class_=re.compile("Num Waku"))
    Wakus = []
    for i in range(1, 16):
        Waku = soup.find_all('td', class_="Waku" +str(i)+" Txt_C")
        if Waku != []:
            for j in range(len(Waku)):
                Wakus.append(Waku[j])
            #end
        #end
    #end
    
    Wakus_list = []
    for Waku in Wakus:
        Waku_ = Waku.get_text().lstrip().rstrip('\n')
        #リスト作成
        Wakus_list.append(Waku_)
    #end

    # ------------------------------------
    # 馬番取得
    # ------------------------------------
    horsenum_list = []
    for i in range(1, 16):
        horsenum = soup.find_all('td', class_="Umaban"+str(i)+" Txt_C")
        if horsenum != []:
            for j in range(len(horsenum)):
                horsenum_list.append(horsenum[j])
            #end
        #end
    #end

    horsenums_list = []
    for horsenum in horsenum_list:
        horsenum_ = horsenum.get_text().lstrip().replace('\n','')
        #リスト作成
        horsenums_list.append(horsenum_)
    #end

    # ------------------------------------
    #コース,距離取得
    # ------------------------------------
    Distance_Course = soup.find_all('span')
    Distance_Course = re.search(r'.[0-9]+m', str(Distance_Course))
    Course = Distance_Course.group()[0]
    Distance = re.sub("\\D", "", Distance_Course.group())

    # ------------------------------------
    # 発走時刻，天気，馬場，
    # ------------------------------------
    RaceData01 = soup.find_all('div', class_='RaceData01')
    RaceData01 = str(RaceData01[0])
    RaceData01  = RaceData01.split("\n")
    
    """
    RaceData01 = ['<div class="RaceData01">',
                '09:55発走 /<!-- <span class="Turf"> --><span> 芝1800m</span> (右)',
                '/ 天候:曇<span class="Icon_Weather Weather02"></span>',
                '<span class="Item03">/ 馬場:良</span>',
                '</div>']
    """
    StartTime    = RaceData01[1].split("発走")[0]
    # Weather      = (RaceData01[2].split("天候:")[1]).split("<")[0]
    # RidingGround = (RaceData01[3].split("馬場:")[1]).split("<")[0]
    Weather      = "晴"
    RidingGround = "良"

    # ------------------------------------
    # 棄権等の調整
    # ------------------------------------
    if len(kiken_list) > 0:
        print(kiken_list)
        for i in range(len(kiken_list)):
            if kiken_list[i] < len(horsenum_list):
                Weights_list.insert(kiken_list[i], '0')
                Ninkis_list.insert(kiken_list[i], '0')
                Odds_Ninkis_list.insert(kiken_list[i], '0')
                Olds_list.insert(kiken_list[i], '0')

                Horse_Names_list[kiken_list[i]] = '0'
                Trainers_list[kiken_list[i]] = '0'
                JockeyWeights_list[kiken_list[i]] = '0'
            #end
        #end
    #end
    
    # ------------------------------------
    # ------------------------------------
    n = len(Wakus_list)
    Ranks_list = [0] * n
    Order_list = [0] * n

    print("----------------")
    print(Ranks_list)
    print(Wakus_list)
    print(Horse_Names_list)
    print(Trainers_list)
    print(Weights_list)
    print(Olds_list)
    print(JockeyWeights_list)
    print(Course)
    print(Distance)
    print(Weather)
    print(RidingGround)
    print(Ninkis_list)
    print(Odds_Ninkis_list)
    print(Order_list)
    print(horsenums_list)
    print("----------------")
    # ------------------------------------
    # ------------------------------------
    df = pd.DataFrame({
        'レースID':''.join(id),
        '順位':Ranks_list,
        '枠':Wakus_list,
        '馬名':Horse_Names_list,
        '騎手名':Trainers_list,
        '体重':Weights_list,
        '年齢':Olds_list,
        '斤量':JockeyWeights_list,
        'コース':Course,
        '距離':Distance,
        '発走':StartTime,
        '天候':Weather,
        '馬場':RidingGround,
        '人気':Ninkis_list,
        'オッズ':Odds_Ninkis_list,
        'コーナー通過順':Order_list,
        '馬番':horsenums_list,
    })
    
    result_df = pd.concat([result_df,df],axis=0)

    # ------------------------------------
    # ------------------------------------
    # print(sys.exc_info())
    # print(race_id)
    # print("サイト取得エラー")
    
    # ------------------------------------
    # elapsed time
    # ------------------------------------
    ite += 1
    elapsed_time = time.time() - start
    print(str(len(id)) +  \
            " : {:.2f}".format(elapsed_time) + " s")
    
    # ------------------------------------
    # output
    # ------------------------------------
    if result_df.empty == False:
        f = dname + "\\" + id
        result_df.to_csv(f, encoding="utf-8")
    #end
    
    return dt_now.strftime('%Y%m%d%H%M%S'), dname, StartTime, e
#end

# ------------------------------------
# ------------------------------------
if __name__ == "__main__":
    main_copy("202204030101")