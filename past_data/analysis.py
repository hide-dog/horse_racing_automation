# ------------------------------------------------
# Macine Learnig     : neural network
# Target Competition : horse racing
# Score              : 
# 
# ------------------------------------------------

# ------------------------------------------------
# import
# ------------------------------------------------
import pandas as pd
import numpy as np
import glob
from tqdm import tqdm
import pickle
import matplotlib.pyplot as plt


# neural_network, random forest
from sklearn import neural_network
from sklearn.ensemble import RandomForestClassifier

# lightGBM
import lightgbm as lgb

from sklearn import preprocessing

# ------------------------------------------------
# read
# ------------------------------------------------
def read_files_temp():
    fin = "re_data/2021_data/*/*"
    # read data
    fff_info   = glob.glob( fin + "_info")
    fff_result = glob.glob( fin + "_result")
    # fff_info   = glob.glob("re_data/2021_data/01/202101010101_info")
    # fff_result = glob.glob("re_data/2021_data/01/202101010101_result")
    
    redata_info = []
    test_info = []
    test_result = []
    test_resultdata = []
    for l in tqdm(range(len(fff_info))):
        temp_info   = np.loadtxt(fff_info[l],   delimiter=",", skiprows=0, usecols=None, unpack=True, ndmin=0)
        temp_result = np.loadtxt(fff_result[l], delimiter=",", skiprows=0, usecols=None, unpack=True, ndmin=0)
        
        redata_info.append(temp_info.tolist())
        
        temp_info = preprocessing.scale((temp_info.T).tolist())
        temp_info = (np.array(temp_info).T).tolist()
        
        test_info.append(temp_info)
        temp_result = temp_result.tolist()
        test_resultdata.append(temp_result)
        test_result.append(temp_result[0])
    #end
    test_info = np.array(test_info)
    test_result = np.array(test_result)
    redata_info = np.array(redata_info)

    return test_info, test_result, test_resultdata, redata_info
#end

# ------------------------------------------------
# main
# ------------------------------------------------
def main():   
    print(" ------------------------------ ")
    print(" start read data")
    
    test_info, test_result, test_resultdata, redata_info = read_files_temp() 

    print(" end read data")
    print(" ------------------------------ ")

    # confirm size of array
    test_shape = test_info.shape
    redata_shape = redata_info.shape
    
    # reshape
    test_nd  = test_shape[1]  * test_shape[2]
    test_info  = np.reshape(test_info,  [test_shape[0],  test_nd])
    redata_nd = redata_shape[1]  * redata_shape[2]
    redata_info  = np.reshape(redata_info,  [redata_shape[0],  redata_nd])

    # get the explanatory variables for "test"
    explanatory_test = test_info

    
    # machine learning
    dir = "model/"
    year = "2020"
    for m in range(3):
        if m == 0:
            model_name = dir + 'neural_network_' + year + '.sav'
        elif m == 1:    
            model_name = dir + 'RandomForest_' + year + '.sav'
        elif m == 2:    
            model_name = dir + 'lightgbm_' + year + '.sav'
        #end

        # 保存したモデルをロードする
        clf = pickle.load(open(model_name, 'rb'))
    
        # prediction
        prediction = clf.predict(explanatory_test)
        
        # accuracy
        print("  ")
        print("  ")
        print("  ")
        print(" ------------------------------ ")
        print(model_name)
        print(" accuracy of test data")
        print("  " + str(clf.score(explanatory_test, test_result)) )
        print(" ------------------------------ ")

        # ----------------------------------    
        # analysis
        # ----------------------------------
        maxn = 16
        rieki = 0
        ite_acc = 0
        ite_all = 0
        for i in range(len(explanatory_test)):
            ite_recover = 0
            temp = clf.predict_proba([explanatory_test[i]])
            jlist = []

            for j in range(maxn):
                recover_rate = redata_info[i][18*13 + j] * temp[0][j]
                
                if recover_rate > 1.0:
                    ite_recover += 1
                    jlist.append(j)
                #end
            #end

            if ite_recover > 0:
                for j in jlist:
                    ite_all += 1
                    if test_result[i] == j+1:
                        rieki += 100 * redata_info[i][18*13 + j]
                        if redata_info[i][18*13 + j] / len(jlist) > 1.0:
                            ite_acc +=1
                        #end
                    #end
                #end
            #end
        #end
        
        print("----------------------------")
        print(" 回収率 = オッズ*機械学習による勝率 > 1.0 を超えた馬全てに 100円 ずつかける場合")
        print(" 投資金：" + str(-ite_all*100))
        print(" 回収金：" + str(rieki))
        print(" 回収率：" + str(rieki / (ite_all*100)))
        print("----------------------------")

        # ----------------------------------
        # ana2
        # ----------------------------------
        maxn = 16
        rieki = 0
        st_big = 0
        censoring_max_odds = 10
        
        ite_all = 0
        for i in range(len(redata_info)):
            temp = clf.predict_proba([explanatory_test[i]])
            ite_all += 1
            
            be_rieki = rieki

            if test_result[i] == (temp[0].tolist()).index(max(temp[0])):
                rieki += 100 * redata_info[i][18*13 + int(test_result[i])-1]
            #end

            af_rieki = rieki
            
            diff = af_rieki - be_rieki
            if diff > 100*censoring_max_odds:
                #print(i)
                #print(diff)
                st_big += diff
            #end
        #end

        print("----------------------------")
        print(" 回収率 によらず全試合の一番確率の高いものに 100円 投資した場合")
        print(" 投資金：" + str(-ite_all*100))
        print(" 回収金：" + str(rieki))
        print(" 回収率：" + str(rieki / (ite_all*100)))
        print(" 回収金(" + str(censoring_max_odds) + "倍を除く)：" + str(rieki - st_big))
        print(" 回収率(" + str(censoring_max_odds) + "倍を除く)：" + str((rieki - st_big) / (ite_all*100)))
        print("----------------------------")
        
        # ----------------------------------
        # ana3
        # 当たり：if test_result[i] == (temp[0].tolist()).index(max(temp[0])):
        # オッズ：redata_info[i][18*13 + int(test_result[i])-1]
        # ----------------------------------
        rieki_umatann   = 0
        rieki_3renntan  = 0
        rieki_umarenn   = 0
        rieki_3rennpuku = 0
        rieki_3rennpuku_l = []
        rieki_3rennpuku_sum = 0
        rieki_hukusyou  = [0, 0, 0]
        rieki_waido     = 0
        ite_all = 0
        for ii in range(len(redata_info)):
            temp = clf.predict_proba([explanatory_test[i]])
            trev = sorted(temp[0], reverse=True)
            temp = temp.tolist()

            pred_rank1 = 1 + temp[0].index(trev[0])   # 予測の1位の馬番号
            pred_rank2 = 1 + temp[0].index(trev[1])   # 予測の2位の馬番号
            pred_rank3 = 1 + temp[0].index(trev[2])   # 予測の3位の馬番号

            real_rank1 = test_resultdata[ii][0]        # 実際の1位の馬番号
            real_rank2 = test_resultdata[ii][1]        # 実際の2位の馬番号
            real_rank3 = test_resultdata[ii][2]        # 実際の3位の馬番号
            
            odds1 = redata_info[ii][13*18 + int(real_rank1)-1] # 実際の1位のオッズ
            odds2 = redata_info[ii][13*18 + int(real_rank2)-1] # 実際の2位のオッズ
            odds3 = redata_info[ii][13*18 + int(real_rank3)-1] # 実際の3位のオッズ

            # if m == 0:
            #     print("------------")
            #     print(temp)
            #     print(test_resultdata)
            #     print(real_rank1)                
            #     print(redata_info[ii][13*18 + int(real_rank1)-1])
        

            if odds1 == 0 or odds2 == 0 or odds3 == 0:
                continue
            #end
            
            pl = []
            for j in range(len(test_resultdata[ii])):
                ol = redata_info[ii][13*18 + int(test_resultdata[ii][j])-1]
                if ol == 0:
                    pl.append(0)
                else:
                    pl.append(1 / (1 + ol))
                #end
            #end

            # ------------------------
            # Harville(1973)            
            # ------------------------
            ite_all += 1
            p1 = 1 / (1 + odds1) # rate
            p2 = 1 / (1 + odds2) # rate
            p3 = 1 / (1 + odds3) # rate
            
            # 馬単
            if real_rank1 == pred_rank1 and real_rank2 == pred_rank2:
                p = p1 * p2 / (1-p1)
                fin_odds = (p / (1-p))**-1
                if fin_odds < 1.0:
                    fin_odds = 1.0
                #end
                rieki_umatann += 100 * fin_odds
            #end
            
            # 三連単
            if real_rank1 == pred_rank1 and real_rank2 == pred_rank2 and real_rank3 == pred_rank3:
                p = p1 * p2 * p3 / (1-p1) / (1-p1-p2)
                fin_odds = (p / (1-p))**-1
                if fin_odds < 1.0:
                    fin_odds = 1.0
                #end
                rieki_3renntan += 100 * fin_odds
            #end

            # 馬連
            if (real_rank1 == pred_rank1 or real_rank1 == pred_rank2) and (real_rank2 == pred_rank1 or real_rank2 == pred_rank2):
                p = p1 * p2 / (1-p1) + p1 * p2 / (1-p2)
                fin_odds = (p / (1-p))**-1
                if fin_odds < 1.0:
                    fin_odds = 1.0
                #end
                rieki_umarenn += 100 * fin_odds
            #end

            # 三連複
            ite = 0
            if (real_rank1 == pred_rank1 or real_rank1 == pred_rank2 or real_rank1 == pred_rank3) and \
               (real_rank2 == pred_rank1 or real_rank2 == pred_rank2 or real_rank2 == pred_rank3) and \
               (real_rank3 == pred_rank1 or real_rank3 == pred_rank2 or real_rank3 == pred_rank3):
                p = p1 * p2 * p3 * \
                    ( 1 / ((1-p1) * (1-p1-p2)) + 1 / ((1-p1) * (1-p1-p3)) + \
                      1 / ((1-p2) * (1-p2-p1)) + 1 / ((1-p2) * (1-p2-p3)) + \
                      1 / ((1-p3) * (1-p3-p2)) + 1 / ((1-p3) * (1-p3-p1)))
                fin_odds = (p / (1-p))**-1
                if fin_odds < 1.0:
                    fin_odds = 1.0
                #end
                rieki_3rennpuku += 100 * fin_odds
                ite = 100 * fin_odds
                print(fin_odds)
            #end
            rieki_3rennpuku_sum -= 100
            rieki_3rennpuku_sum += ite
            rieki_3rennpuku_l.append(rieki_3rennpuku_sum)

            # 複勝
            b = [0,0,0]
            if (real_rank1 == pred_rank1 or real_rank1 == pred_rank2 or real_rank1 == pred_rank3) or \
               (real_rank2 == pred_rank1 or real_rank2 == pred_rank2 or real_rank2 == pred_rank3) or \
               (real_rank3 == pred_rank1 or real_rank3 == pred_rank2 or real_rank3 == pred_rank3):
                
                if (pred_rank1 == real_rank1 or pred_rank1 == real_rank2 or pred_rank1 == real_rank3):
                    b[0] = 1
                if (pred_rank2 == real_rank1 or pred_rank2 == real_rank2 or pred_rank2 == real_rank3):
                    b[1] = 1
                if (pred_rank3 == real_rank1 or pred_rank3 == real_rank2 or pred_rank3 == real_rank3):
                    b[2] = 1
                #end

                for n in range(3):
                    p = 0
                    
                    # 1位の確率
                    p += pl[n]
                    
                    # 2位の確率
                    for i in range(len(pl)):
                        if i == n or pl[i] == 0:
                            continue
                        #end
                        p += pl[n] * pl[i] / (1-pl[i])
                    #end
                    
                    # 3位の確率
                    for i in range(len(pl)):
                        for j in range(len(pl)):
                            if i == j or i == n or j == n or pl[i] == 0:
                                continue
                            #end
                            p += pl[0] * pl[i] * pl[j] / (1-pl[i])/(1-pl[i]-pl[j])
                        #end
                    #end

                    fin_odds = (p / (1-p))**-1
                    if fin_odds < 1.0:
                        fin_odds = 1.0
                    #end
                    rieki_hukusyou[n] += 100 * fin_odds * b[n]
                #end
            #end

            # ワイド
            if ((real_rank1 == pred_rank1 or real_rank1 == pred_rank2) and (real_rank2 == pred_rank1 or real_rank2 == pred_rank2)) or \
               ((real_rank2 == pred_rank1 or real_rank2 == pred_rank2) and (real_rank3 == pred_rank1 or real_rank3 == pred_rank2)) or \
               ((real_rank1 == pred_rank1 or real_rank1 == pred_rank2) and (real_rank3 == pred_rank1 or real_rank3 == pred_rank2)):
                p = 0
                # 1,2位の確率
                p += pl[0] * pl[1] / (1-pl[0])
                # 2,1位の確率
                p += pl[1] * pl[0] / (1-pl[1])
                
                for i in range(2, len(pl)):
                    p += pl[i] * pl[0] * pl[1] / (1-pl[i])/(1-pl[i]-pl[0]) # 2,3位の確率
                    p += pl[i] * pl[1] * pl[0] / (1-pl[i])/(1-pl[i]-pl[1]) # 3,2位の確率
                    p += pl[0] * pl[i] * pl[1] / (1-pl[0])/(1-pl[0]-pl[i]) # 1,3位の確率
                    p += pl[1] * pl[i] * pl[0] / (1-pl[1])/(1-pl[1]-pl[i]) # 3,1位の確率
                #end
                
                fin_odds = (p / (1-p))**-1
                if fin_odds < 1.0:
                    fin_odds = 1.0
                #end
                rieki_waido += 100 * fin_odds
            #end
        #end

        print("----------------------------")
        print(" 投資金：" + str(-ite_all*100))
        print(" 複勝で3位までに常に100円かけた場合")
        print(" 回収金：" + str(rieki_hukusyou[0]))
        print(" 回収率：" + str(rieki_hukusyou[0] / (ite_all*100)))
        print(" 回収金：" + str(rieki_hukusyou[1]))
        print(" 回収率：" + str(rieki_hukusyou[1] / (ite_all*100)))
        print(" 回収金：" + str(rieki_hukusyou[2]))
        print(" 回収率：" + str(rieki_hukusyou[2] / (ite_all*100)))
        print(" ワイドで1,2位に常に100円かけた場合")
        print(" 回収金：" + str(rieki_waido))
        print(" 回収率：" + str(rieki_waido / (ite_all*100)))
        print(" 馬単で常に100円かけた場合")
        print(" 回収金：" + str(rieki_umatann))
        print(" 回収率：" + str(rieki_umatann / (ite_all*100)))
        print(" 馬連で常に100円かけた場合")
        print(" 回収金：" + str(rieki_umarenn))
        print(" 回収率：" + str(rieki_umarenn / (ite_all*100)))
        print(" 3連単で常に100円かけた場合")
        print(" 回収金：" + str(rieki_3renntan))
        print(" 回収率：" + str(rieki_3renntan / (ite_all*100)))
        print(" 3連複で常に100円かけた場合")
        print(" 回収金：" + str(rieki_3rennpuku))
        print(" 回収率：" + str(rieki_3rennpuku / (ite_all*100)))
        print("----------------------------")
        
        num_race_l = np.zeros(len(rieki_3rennpuku_l))
        for i in range(len(num_race_l)):
            num_race_l[i] = i
        #end

        plt.scatter(num_race_l, rieki_3rennpuku_l, s=1, marker="o", c = "b", alpha=1)

        plt.grid()
        plt.rcParams['axes.axisbelow'] = True
        # plt.xlim([0, 10422.6])
        # plt.ylim([-60, 60])
        plt.xlabel("Number of races", fontsize=14)
        plt.ylabel("Profit, yen", fontsize=14)
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
        tn = model_name.replace('_' + year + '.sav',"")
        tn = tn.replace(dir,"")
        plt.title(tn, fontsize=14)
        plt.tight_layout()

        plt.savefig("rieki_sannrennpuku_" + str(m) + ".png", format="png")
        plt.clf()
    #end
#end

# ------------------------------------------------
# ------------------------------------------------
if __name__ == "__main__":
    main()