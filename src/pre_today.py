# ------------------------------------
# import
# ------------------------------------
import glob
import copy
import datetime
import os
# ------------------------------------
# main
# ------------------------------------
def pre(dname):
    # ------------------------------------
    # input files
    # ------------------------------------
    fff = glob.glob(dname + "/*")
    fff = [i for i in fff if i.find("_info") == -1 and i.find("_result") == -1]
    
    # ------------------------------------
    # lists
    # ------------------------------------
    with open("hn_data", "r") as f:
        hn = f.readlines()
    #end
    with open("tn_data", "r") as f:
        tn = f.readlines()
    #end
    hn_ite = 1 + len(hn)
    tn_ite = 1 + len(tn)

    max_hn = 18
    maxn = 0
    
    # ------------------------------------
    # loop f
    # ------------------------------------
    for l in range(len(fff)):
        # ------------------------------------
        # read files
        # ------------------------------------    
        with open(fff[l], encoding="utf-8") as f:
            lines = f.readlines()
        #end
        
        # trim data
        n = len(lines)
        e_num = 0
        for linei in range(n):
            e_num += lines[linei].count("取消")
            e_num += lines[linei].count("除外")
            e_num += lines[linei].count("中止")
        #end
        
        # ------------------------------------
        # refine
        # ------------------------------------
        # ,レースID,順位,枠,馬名,騎手名,体重,年齢,斤量,コース,距離,発走,天候,馬場,人気,オッズ,コーナー通過順,馬番
        n = len(lines)-1 - e_num
        horsenum_list = []
        try:
            for linei in range(n): 
                # 0,200801010101,1,4,ディアジーナ,美浦田村,468(0),牝2,54.0,
                # 芝,1500,10:40,曇,良,2,4.3,2-3-5,1
                temp = lines[linei+1].split(",")

                # horse name
                if temp[4] == "0":
                    temp[4] = 0
                    pass
                elif temp[4] in hn:
                    temp[4] = hn.index(temp[4]) + 1 # index番号の取得
                else:
                    # hn.append(temp[4])          # 馬名の追加
                    temp[4] = hn_ite
                    hn_ite += 1
                #end
                temp[4] = str(temp[4])

                # trainer name
                if temp[5] in tn:
                    temp[5] = tn.index(temp[5]) # index番号の取得
                else:
                    # tn.append(temp[5])          # 騎手の追加
                    temp[5] = tn_ite
                    tn_ite += 1
                #end
                temp[5] = str(temp[5])

                # weight
                weight = temp[6].split("(")[0]
                if weight == "":
                    weight = "500"
                #end
                
                # delta weight
                try:
                    dw = ((temp[6].split("(")[1]).split(")")[0]).replace("+","")
                except:
                    dw = str(0)
                #end

                # old
                old = temp[7].replace("牝","")
                old = old.replace("牡","")
                old = old.replace("セ","")

                # place
                if temp[9] == "芝":
                    place = 1
                elif temp[9] == "ダ":
                    place = 2
                elif temp[9] == "障":
                    place = 3
                else:
                    print(" 場所に関して，分類できていません \n ")
                    print(temp[9])
                    raise ValueError("error!")
                #end
            
                place = str(place)

                # start time
                temp[11] = temp[11].replace(" ","")
                if len(temp[11]) == 4:
                    temp[11] = "0" + temp[11][0] + temp[11][2] + temp[11][3]
                elif len(temp[11]) == 5:
                    temp[11] = temp[11][0] + temp[11][1] + temp[11][3] + temp[11][4]
                #end

                # weather
                if temp[12] == "曇":
                    weather = 1
                elif temp[12] == "晴":
                    weather = 2
                elif temp[12] == "雨":
                    weather = 3
                elif temp[12] == "小雨":
                    weather = 4
                elif temp[12] == "小雪":
                    weather = 5
                elif temp[12] == "雪":
                    weather = 6
                else:
                    print(" 天気に関して，分類できていません \n ")
                    print(temp[12])
                    raise ValueError("error!")
                #end
                weather = str(weather)

                # place evaluation
                if temp[13] == "良":
                    place_e = 1
                elif temp[13] == "稍":
                    place_e = 2
                elif temp[13] == "不":
                    place_e = 3
                elif temp[13] == "重":
                    place_e = 4
                else:
                    print(" 場所の評価に関して，分類できていません \n ")
                    print(temp[13])
                    raise ValueError("error!")
                #end
                place_e = str(place_e)
            
                # order corners 
                temp[16] = temp[16].replace("-", ",")

                # gather
                lines[linei+1] = ""
                
                #lines[linei+1] += temp[1] + ","
                #lines[linei+1] += temp[2] + ","
                lines[linei+1] += temp[3] + ","
                lines[linei+1] += temp[4] + ","
                lines[linei+1] += temp[5] + ","
                lines[linei+1] += weight  + ","
                lines[linei+1] += dw      + ","
                lines[linei+1] += old     + ","
                lines[linei+1] += temp[8] + ","
                lines[linei+1] += place   + ","
                lines[linei+1] += temp[10] + ","
                lines[linei+1] += temp[11] + ","
                lines[linei+1] += weather  + ","
                lines[linei+1] += place_e  + ","
                lines[linei+1] += temp[14] + ","
                lines[linei+1] += temp[15] + ","
                #lines[linei+1] += temp[16]
                lines[linei+1] += temp[17]


                horsenum_list.append(temp[17].replace("\n",""))
            #end

            tlines = copy.deepcopy(lines)
            for linei in range(n):
                stn = int(horsenum_list[linei])
                lines[stn] = tlines[ linei+1 ]
            #end

            # ------------------------------------
            # prepare
            # ------------------------------------
            dn = lines[1].count(",") + 1
            plines = ""
            for i in range(dn - 2):
                plines += "0" + ","
            #end
            plines += "0"

            # ------------------------------------
            # output
            # ------------------------------------
            fout = fff[l] + "_info"
            print(fout)
            with open(fout, "w+", encoding="utf-8") as f:
                for linei in range(max_hn):
                    if linei < n and lines[linei+1][0] != "0":
                        f.write(lines[linei+1])
                    else:
                        f.write(plines + "," + str(linei+1) + "\n")
                    #end
                #end
            #end
            
            fout = fff[l] + "_result"
            with open(fout, "w+", encoding="utf-8") as f:
                for i in range(len(horsenum_list)):
                    f.write(horsenum_list[i])
                    f.write("\n")
                #end
            #end

            if maxn < n:
                maxn = n
            #end
        except:
            # print(temp)
            pass
        #end
    #end

    print(" -------------------- ")
    print(" 最大データ数 \n ")
    print(maxn)
    print(" -------------------- ")

    # output hh, ht, 
    # with open("hn_data", "w") as f:
    #     for i in range(len(hn)):
    #         f.write(hn[i])
    #         f.write("\n")
    #     #end
    # #end
    # with open("tn_data", "w") as f:
    #     for i in range(len(tn)):
    #         f.write(tn[i])
    #         f.write("\n")
    #     #end
    # #end
#end
# ------------------------------------
# ------------------------------------
if __name__ == "__main__":
    pre()