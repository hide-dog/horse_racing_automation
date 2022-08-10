# ------------------------------------
# horse_racing
# ------------------------------------

# ------------------------------------
# スクレイピングに必要なモジュール
# ------------------------------------
import requests
from bs4 import BeautifulSoup
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

# ------------------------------------
# main
# ------------------------------------
def main():
    # ------------------------------------
    # レースIDの作成
    # ------------------------------------
    # YEAR = ['2021']
    # CODE = ['01'] # 競馬場id
    # RACE_COUNT = ['01']
    # DAYS = ['01']
    # RACE_NUM = ['01'] # 12 race

    YEAR = [str(num+2008) for num in range(14)]
    CODE = [str(num+1).zfill(2) for num in range(10)]       # 競馬場id 中央競馬場 10
    RACE_COUNT = [str(num+1).zfill(2) for num in range(6)]  # 6  (number of months per year)
    DAYS = [str(num+1).zfill(2) for num in range(10)]       # 10 (number of days per month)
    RACE_NUM = [str(num+1).zfill(2) for num in range(12)]   # 12 race

    race_ids = list(itertools.product(YEAR,CODE,RACE_COUNT,DAYS,RACE_NUM))

    print("get " + str(len(race_ids)) + " data")

    # サイトURLの作成
    SITE_URL = ["https://race.netkeiba.com/race/result.html?race_id={}".format(''.join(race_id)) for race_id in race_ids]

    # ------------------------------------
    # ------------------------------------
    #サイトURLをループしてデータを取得する
    ite = 0
    for sitename,race_id in zip(SITE_URL,race_ids):
        result_df = pd.DataFrame()
        start = time.time()
        # ------------------------------------
        # ------------------------------------
        try:
            # スクレイピング対象の URL にリクエストを送り HTML を取得する
            res = requests.get(sitename)
            res.raise_for_status()  #URLが正しくない場合，例外を発生させる

            # 時間をあけてアクセスするように、sleepを設定する
            time.sleep(1.1)
            
            # レスポンスの HTML から BeautifulSoup オブジェクトを作る
            soup = BeautifulSoup(res.content, 'html.parser')
            
            # title タグの文字列を取得する
            title_text = soup.find('title').get_text()
            
            # ------------------------------------
            #順位のリスト作成
            # ------------------------------------
            Ranks = soup.find_all('div', class_='Rank')
            Ranks_list = []
            for Rank in Ranks:
                Rank = Rank.get_text()
                #リスト作成
                Ranks_list.append(Rank)
            #end
            
            # ------------------------------------
            #馬名取得
            # ------------------------------------
            Horse_Names = soup.find_all('span', class_='Horse_Name')
            Horse_Names_list = []
            for Horse_Name in Horse_Names:
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
            Olds = soup.find_all('span', class_='Lgt_Txt Txt_C')
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
            JockeyWeights = soup.find_all('span', class_='JockeyWeight')
            JockeyWeights_list = []
            for JockeyWeight in JockeyWeights:
                #馬名のみ取得(lstrip()先頭の空白削除，rstrip()改行削除)
                JockeyWeight = JockeyWeight.get_text().lstrip().rstrip('\n')
                #リスト作成
                JockeyWeights_list.append(JockeyWeight)
            #end

            # ------------------------------------
            #人気取得
            # ------------------------------------
            Ninkis = soup.find_all('span', class_='OddsPeople')
            Ninkis_list = []
            for Ninki in Ninkis:
                Ninki = Ninki.get_text()
                #リスト作成
                Ninkis_list.append(Ninki)
            #end

            # ------------------------------------
            #オッズ取得
            # ------------------------------------
            Odds_Ninkis = soup.find_all('td', class_='Odds Txt_R')
            Odds_Ninkis_list = []
            ite_odds = 0
            for Odds_Ninki in Odds_Ninkis:
                #Odds_Ninki = Odds_Ninki.get_text()
                Odds_Ninki = str(Odds_Ninkis[ite_odds])
                Odds_Ninki  = Odds_Ninki.replace("\n","")
                Odds_Ninki  = Odds_Ninki.replace("\"","")
                Odds_Ninki  = (Odds_Ninki.split(">")[2]).split("<")[0]
                #リスト作成
                Odds_Ninkis_list.append(Odds_Ninki)

                ite_odds +=1
            #end

            # ------------------------------------
            #コーナー通過
            # ------------------------------------
            Orders = soup.find_all('td', class_='PassageRate')
            Order_list = []
            for Order in Orders:
                #馬名のみ取得(lstrip()先頭の空白削除，rstrip()改行削除)
                Order = Order.get_text().lstrip().rstrip('\n')
                #リスト作成
                Order_list.append(Order)
            #end
            
            # ------------------------------------
            #枠取得
            # ------------------------------------
            Wakus = soup.find_all('td', class_=re.compile("Num Waku"))
            Wakus_list = []
            for Waku in Wakus:
                Waku = Waku.get_text().replace('\n','')
                #リスト作成
                Wakus_list.append(Waku)
            #end

            # ------------------------------------
            # 馬番取得
            # ------------------------------------
            horsenums = soup.find_all('td', class_="Num Txt_C")
            horsenums_list = []
            for horsenum in horsenums:
                horsenum = horsenum.get_text().replace('\n','')
                #リスト作成
                horsenums_list.append(horsenum)
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
            # ------------------------------------
            df = pd.DataFrame({
                'レースID':''.join(race_id),
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
        except:
            print(sys.exc_info())
            print(race_id)
            print("サイト取得エラー")
        
        # ------------------------------------
        # elapsed time
        # ------------------------------------
        ite += 1
        elapsed_time = time.time() - start
        print(str(ite) + " / " + str(len(race_ids)) +  \
                " : {:.2f}".format(elapsed_time) + " s")
        
        # ------------------------------------
        # output
        # ------------------------------------
        if result_df.empty == False:
            Rid = ""
            for j in range(5):
                Rid += race_id[j]
            #end
            
            f = "raw_data/" + race_id[0] + "_data/" + race_id[1] + "/" + Rid
            result_df.to_csv(f, encoding="utf-8")
        #end
    #end
#end


# ------------------------------------
# ------------------------------------
main()