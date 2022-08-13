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
    
    YEAR = ["2021"]
    # YEAR = [str(num+2008) for num in range(14)]
    CODE = [str(num+1).zfill(2) for num in range(9)]       # 競馬場id 中央競馬場 10
    RACE_COUNT = [str(num+1).zfill(2) for num in range(6)]  # 6  (number of months per year)
    DAYS = [str(num+1).zfill(2) for num in range(10)]       # 10 (number of days per month)
    RACE_NUM = [str(num+1).zfill(2) for num in range(12)]   # 12 race

    # CODE = ["04"]       # 競馬場id 中央競馬場 10
    # RACE_COUNT = ["02"]  # 6  (number of months per year)
    # DAYS = ["04"]       # 10 (number of days per month)
    # RACE_NUM = ["01"]   # 12 race

    race_ids = list(itertools.product(YEAR,CODE,RACE_COUNT,DAYS,RACE_NUM))

    print("get " + str(len(race_ids)) + " data")

    # サイトURLの作成
    SITE_URL = ["https://race.netkeiba.com/race/result.html?race_id={}".format(''.join(race_id)) for race_id in race_ids]

    # ------------------------------------
    # ------------------------------------
    #サイトURLをループしてデータを取得する
    ite = 0
    for sitename, race_id in zip(SITE_URL, race_ids):
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
            
            # ------------------------------------
            # 支払い
            # ------------------------------------
            Payout = soup.find_all('td', class_='Payout')
            Payout_list = []
            for P in Payout:
                P = P.get_text()
                P = P.split("円")
                #リスト作成
                for i in range(len(P)-1):
                    Payout_list.append(P[i])
                #end
            #end
            print(Payout_list)
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
        if Payout_list != []:
            Rid = ""
            for j in range(5):
                Rid += race_id[j]
            #end
            f = "raw_data/" + race_id[0] + "_data/" + race_id[1] + "/" + Rid + "_payout"      
            print(f)
            with open(f, "w") as f:
                f.write("単勝, 複勝1, 複勝2, 複勝3, 枠連, 馬連, ワイド1-2, ワイド1-3, ワイド2-3, 馬単, 3連複, 3連単")
                f.write("\n")
                for i in range(len(Payout_list)):
                    f.write(Payout_list[i])
                    f.write("\n")
                #end
            #end
        #end
    #end
#end


# ------------------------------------
# ------------------------------------
main()