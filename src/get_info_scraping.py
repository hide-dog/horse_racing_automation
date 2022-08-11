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
def only_get_time(id):

    sitename = "https://race.netkeiba.com/race/shutuba.html?race_id={}".format(id)

    # スクレイピング対象の URL にリクエストを送り HTML を取得する
    res = requests.get(sitename)
    res.raise_for_status()  #URLが正しくない場合，例外を発生させる

    # 時間をあけてアクセスするように、sleepを設定する
    time.sleep(1.1)
    
    # レスポンスの HTML から BeautifulSoup オブジェクトを作る
    soup = BeautifulSoup(res.content, 'html.parser')

    RaceData01 = soup.find_all('div', class_='RaceData01')
    RaceData01 = str(RaceData01[0])
    RaceData01  = RaceData01.split("\n")
    
    StartTime    = RaceData01[1].split("発走")[0]
    # print(RaceData01)
    return StartTime
#end

def get_id(id = "0"):
    # ------------------------------------
    # 当日のIDの作成
    # ------------------------------------
    # サイトURLの作成
    date = datetime.datetime.now()
    y = date.year
    m = date.month
    d = date.day
    SITE_URL = "https://race.netkeiba.com/top/race_list.html?kaisai_date=" + str(y) + str(m).zfill(2) + str(d).zfill(2)

    if id != "0":
        SITE_URL = "https://race.netkeiba.com/top/race_list.html?kaisai_date=" + id
    #end


    # ------------------------------------
    # ------------------------------------
    id_list = []
    # start = time.time()
    # ------------------------------------
    # ------------------------------------
    # スクレイピング対象の URL にリクエストを送り HTML を取得する
    res = requests.get(SITE_URL)
    res.raise_for_status()  #URLが正しくない場合，例外を発生させる
    # print(res.text) # 全体が見える

    # 時間をあけてアクセスするように、sleepを設定する
    time.sleep(1.1)

    # レスポンスの HTML から BeautifulSoup オブジェクトを作る
    soup = BeautifulSoup(res.content, 'html.parser')
        
    # 動的用セッション開始
    session = HTMLSession()
    r = session.get(SITE_URL)
    # ブラウザエンジンでHTMLを生成させる
    r.html.render(timeout=60)
    
    # ------------------------------------
    # 開催地、回、日目を取得
    # ------------------------------------
    td = r.html.find('.RaceList_DataTitle')
    for i in td:
        tmp = (i.text).split(" ")
        id_list.append([tmp[1], tmp[0].replace("回", ""), tmp[2].replace("日目", "")])
    # #end
    
    # ------------------------------------
    # レース数を取得
    # ------------------------------------
    td = r.html.find('.Race_Num')
    rn_list = []
    tmp_list = []
    for i in td:
        tmp = (i.text).replace("R", "")
        if len(tmp_list) > 1:
            if tmp_list[-1] > int(tmp):
                rn_list.append(tmp_list)
                tmp_list = []
            #end
        #end
        tmp_list.append(int(tmp))
    #end
    rn_list.append(tmp_list)
    
    # ------------------------------------
    # elapsed time
    # ------------------------------------
    # elapsed_time = time.time() - start
    # print(" : {:.2f}".format(elapsed_time) + " s")
    
    # ------------------------------------
    # output
    # ------------------------------------
    return id_list, rn_list
#end

# ------------------------------------
# ------------------------------------
if __name__ == "__main__":
    get_id("202204030101")