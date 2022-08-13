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
import glob
# ------------------------------------
# main
# ------------------------------------
def get_odds(id_list):
    print("start get odds")
    # ------------------------------------
    # レースIDの作成
    # ------------------------------------
    
    # サイトURLの作成
    url = "https://race.netkeiba.com/race/result.html?race_id="

    # ------------------------------------
    # ------------------------------------
    #サイトURLをループしてデータを取得する
    ite = 0
    for id in id_list:
        fff = glob.glob("*today")
        f = ""
        for fi in fff:
            if fi.find(id) > -1:
                f = fi + "/" + id + "_payout"
            #end
        #end
        if f == "":
            continue
        #end
        
        sitename = url + id
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
            print(id)
            print("サイト取得エラー")
        #end
        # ------------------------------------
        # elapsed time
        # ------------------------------------
        ite += 1
        elapsed_time = time.time() - start
        print(str(ite) + " / " + str(len(id_list)) +  \
                " : {:.2f}".format(elapsed_time) + " s")
        
        # ------------------------------------
        # output
        # ------------------------------------
        if Payout_list != []:
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
    print("end get odds")
#end


# ------------------------------------
# ------------------------------------
# get_odds()