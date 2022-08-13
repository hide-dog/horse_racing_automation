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
def get_result(id_list):
    print("start get result")
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
                f = fi + "/" + id + "_result"
            #end
        #end
        if f == "":
            continue
        #end

        sitename = url + id
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
            # ------------------------------------
            df = pd.DataFrame({
                '馬番':horsenums_list,
            })
            
            result_df = pd.concat([result_df,df],axis=0)

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
        if result_df.empty == False:
            result_df.to_csv(f, encoding="utf-8")
        #end
    #end
    print("end get result")
#end