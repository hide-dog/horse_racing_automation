# ------------------------------------------------
# Macine Learnig     : neural network
# Target Competition : horse racing
# Score              : 
# 
# ------------------------------------------------

# ------------------------------------------------
# import
# ------------------------------------------------
import numpy as np
import glob
from tqdm import tqdm
import pickle
import matplotlib.pyplot as plt

from sklearn import preprocessing

# 
year = 2021
line_win = 0.3
line_odds = 5.0
# ------------------------------------------------
# read
# ------------------------------------------------
def read_files_temp():
    fin = "re_data/" + str(year) + "_data/*/*"
    # fin = "re_data/2022_data/*/*"
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

    return test_info, test_result, test_resultdata, redata_info, fff_info
#end

# ------------------------------------------------
# main
# ------------------------------------------------
def main():   
    print(" ------------------------------ ")
    print(" start read data")
    
    test_info, test_result, test_resultdata, redata_info, fff_info = read_files_temp() 

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
    Ym1 = str(year-1)
    # year = "2021"
    fin = glob.glob("raw_data/" + str(year) + "_data/*/*_payout")
    for m in range(4):
        model_name = []
        clf = []
        for rank in range(3):
            if m == 0:
                model_name.append( dir + 'neural_network_' + Ym1 + "_rank"+ str(rank) + '.sav')
            elif m == 1:    
                # model_name.append( dir + 'RandomForest_' + Ym1 + "_rank"+ str(rank) +  '.sav')
                continue
            elif m == 2:    
                model_name.append( dir + 'lightgbm_' + Ym1 + "_rank"+ str(rank) +  '.sav')
            elif m == 3:    
                model_name.append( dir + 'catboost_' + Ym1 + "_rank"+ str(rank) +  '.sav')
            #end
            # 保存したモデルをロードする
            clf.append(pickle.load(open(model_name[rank], 'rb')))
        #end
        if m ==1: # for random
            continue
    
        # # accuracy
        # print("  ")
        # print("  ")
        # print("  ")
        # print(" ------------------------------ ")
        # print(model_name)
        # print(" accuracy of test data")
        # print("  " + str(clf.score(explanatory_test, test_result)) )
        # print(" ------------------------------ ")

        # ----------------------------------
        # 当たり：if test_result[i] == (temp[0].tolist()).index(max(temp[0])):
        # オッズ：redata_info[i][18*13 + int(test_result[i])-1]
        # ----------------------------------
        rieki = 0
        rieki_l = []
        rieki_sum = 0
        pay = 0
        ite_all = 0
        ite_atari = 0
        pred_rank = np.zeros(3)
        nsyoubu = 0
        for ii in range(len(redata_info)):
            
            temp = clf[0].predict_proba([explanatory_test[ii]])
            trev = sorted(temp[0], reverse=True)
            temp = temp.tolist()
            
            ni = temp[0].index(trev[0])
            # pred_rank[0] = ni+1

            # temp = clf[1].predict_proba([explanatory_test[ii]])
            # trev = sorted(temp[0], reverse=True)
            # temp = temp.tolist()
            
            # ni = temp[0].index(trev[1])
            # pred_rank[1] = ni+1

            # temp = clf[2].predict_proba([explanatory_test[ii]])
            # trev = sorted(temp[0], reverse=True)
            # temp = temp.tolist()
            
            # ni = temp[0].index(trev[2])
            # pred_rank[2] = ni+1
            
            odds_input = redata_info[ii][18*13:18*14]
                        
            n = 18 # number of 下位
            pred_rank = np.zeros(n)
            win_rate  = np.zeros(n)
            odds_input_use = np.zeros(n)
            # if len(trev) < n:
            #     continue
            # #end
            
            jj = 0
            for j in range(n):
                ni = temp[0].index(trev[j])
                if odds_input[ni] == 0:
                    jj +=1
                    continue
                else:
                    pred_rank[j-jj] = ni+1   # 予測のj位の馬番号
                    win_rate[j-jj]  = temp[0][int(ni)]
                    odds_input_use[j-jj] = odds_input[ni]
                #end
            #end
            if pred_rank[4] == 0.0: # 最低4つのデータ
                continue
            #end
        
            real_rank1 = test_resultdata[ii][0]        # 実際の1位の馬番号
            real_rank2 = test_resultdata[ii][1]        # 実際の2位の馬番号
            real_rank3 = test_resultdata[ii][2]        # 実際の3位の馬番号
            
            odds1 = redata_info[ii][13*18 + int(real_rank1)-1] # 実際の1位の単勝オッズ
            odds2 = redata_info[ii][13*18 + int(real_rank2)-1] # 実際の2位の単勝オッズ
            odds3 = redata_info[ii][13*18 + int(real_rank3)-1] # 実際の3位の単勝オッズ

            if odds1 == 0 or odds2 == 0 or odds3 == 0:
                continue
            #end
            
            odds = []
            for f in fin:
                if f.find(fff_info[ii][-17:-5]) > -1:
                    with open(f, "r") as ff:
                        l = ff.readlines()
                    #end
                    for k in range(1, len(l)):
                        odds.append(int(l[k].replace(",", ""))/100)
                    #end
                #end
            #end
            if odds == []:
                continue
            #end
            
            # ------------------------
            # Harville(1973)            
            # ------------------------
            # ------------------------
            # ------------------------

            # 1-5, ワイド
            
            ii = 0
            # print(win_rate)
            # print(odds_input_use)
            # exit()
            kk = -1
            for j in range(n):
                
                if win_rate[j] < line_win or odds_input_use[j] < line_odds:
                    continue
                #end
                
                pred_rank1 = pred_rank[j]
                
                ite = 0
                if real_rank1 == pred_rank1:
                    rieki += 100 * odds[0]
                    ite = 100 * odds[0]
                    ii = 1
                #end
                rieki_sum -= 100
                pay += 100
                rieki_sum += ite
                kk = j
            #end
            if kk != -1:
                ite_all += 1
                ite_atari += ii
                nsyoubu += 1
            #end
            rieki_l.append(rieki_sum)
        #end

        print("----------------------------")
        print(" 単勝で常にx00円かけた場合")
        print(" 回収金：" + str(rieki))
        print(" 回収率：" + str(rieki / (pay)))
        print(" 的中率：" + str(ite_atari / ite_all))
        print(" 勝負率：" + str(nsyoubu / len(rieki_l)))
        print("----------------------------")
        
        num_race_l = np.zeros(len(rieki_l))
        for i in range(len(num_race_l)):
            num_race_l[i] = i
        #end

        plt.scatter(num_race_l, rieki_l, s=1, marker="o", c = "b", alpha=1)

        plt.grid()
        plt.rcParams['axes.axisbelow'] = True
        # plt.ticklabel_format(style='sci',axis='y')
        # plt.xlim([0, 10422.6])
        # plt.ylim([-60, 60])
        plt.xlabel("Number of races", fontsize=14)
        # plt.ylabel("Profit, yen", fontsize=14)
        plt.ylabel("rieki, yen", fontsize=14)
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
        # tn = model_name[m].replace('_' + Ym1 + '.sav',"")
        tn = model_name[0]
        tn = tn.replace(dir,"")
        tn += "\n"
        # for i in range(len(pred_rank)):
        #     tn += str(pred_rank[i])
        #     tn += ","
        # #end
        tn += "\n"
        tn += " tansyou : min win ratio " + str(line_win) + " min odds "+ str(line_odds)
        tn += "\n"
        tn += " Recovery money : " + str(rieki)
        tn += "\n"
        tn += " Recovery rate : " + str(rieki / (pay))
        tn += "\n"
        tn += " hitting ratio : " + str(ite_atari / ite_all)
        tn += "\n"
        tn += " bet ratio : " + str(nsyoubu / len(rieki_l))
        tn += "\n"
        plt.title(tn, fontsize=14)
        plt.tight_layout()

        plt.savefig("rieki_tansyou" + "_" + str(year) + "_" + Ym1 + "model_" + str(m) + ".png", format="png")
        # plt.savefig("rieki_sannrennpuku" + "_2022_2021model_" + str(m) + ".png", format="png")
        plt.clf()
    #end
#end

# ------------------------------------------------
# ------------------------------------------------
if __name__ == "__main__":
    main()