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

# 3-7-7, 三連複
year = 2022
ll5 = [1,2,3]

# ll3 = [3,4,5]         # good
# ll7 = [0,1,2,6,7,8,9]  # good
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
        if m == 0:
            model_name = dir + 'neural_network_' + Ym1 + '.sav'
        elif m == 1:    
            model_name = dir + 'RandomForest_' + Ym1 + '.sav'
            continue
        elif m == 2:    
            model_name = dir + 'lightgbm_' + Ym1 + '.sav'
        elif m == 3:    
            model_name = dir + 'catboost_' + Ym1 + '.sav'
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
        # 当たり：if test_result[i] == (temp[0].tolist()).index(max(temp[0])):
        # オッズ：redata_info[i][18*13 + int(test_result[i])-1]
        # ----------------------------------
        rieki = 0
        rieki_l = []
        rieki_sum = 0
        ite_all = 0
        ite_atari = 0
        for ii in range(len(redata_info)):
            temp = clf.predict_proba([explanatory_test[ii]])
            trev = sorted(temp[0], reverse=True)
            temp = temp.tolist()
            
            n = 14 # number of 下位
            pred_rank = np.zeros(n)
            if len(trev) < n:
                continue
            #end
            # print(len(trev))

            for j in range(n):
                pred_rank[j] = 1 + temp[0].index(trev[j])   # 予測のj位の馬番号
            #end

            real_rank1 = test_resultdata[ii][0]        # 実際の1位の馬番号
            real_rank2 = test_resultdata[ii][1]        # 実際の2位の馬番号
            real_rank3 = test_resultdata[ii][2]        # 実際の3位の馬番号
            
            odds1 = redata_info[ii][13*18 + int(real_rank1)-1] # 実際の1位のオッズ
            odds2 = redata_info[ii][13*18 + int(real_rank2)-1] # 実際の2位のオッズ
            odds3 = redata_info[ii][13*18 + int(real_rank3)-1] # 実際の3位のオッズ

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
            if odds == [] or len(odds) < 11:
                continue
            #end
            
            # ------------------------
            # Harville(1973)            
            # ------------------------
            ite_all += 1
            # ------------------------
            # ------------------------

            # 3-7-7, 三連複
            import itertools
            
            combi = list(itertools.combinations(ll5, 3))
            
            ii = 0
            for j in range(len(combi)):
                
                idx = j // 3                   # 0, 0, 0, 1, 1, 1, 2, 2, 2...
                pred_rank1 = pred_rank[combi[idx][0]]
                pred_rank2 = pred_rank[combi[idx][1]]
                pred_rank3 = pred_rank[combi[idx][2]]

                ite = 0
                if (real_rank1 == pred_rank1 or real_rank1 == pred_rank2 or real_rank1 == pred_rank3) and \
                    (real_rank2 == pred_rank1 or real_rank2 == pred_rank2 or real_rank2 == pred_rank3) and \
                    (real_rank3 == pred_rank1 or real_rank3 == pred_rank2 or real_rank3 == pred_rank3):
                    rieki += 100 * odds[10]
                    ite = 100 * odds[10]
                    ii = 1
                #end
                rieki_sum -= 100
                rieki_sum += ite
            #end
            ite_atari += ii
            rieki_l.append(rieki_sum)
        #end

        print("----------------------------")
        print(" 3連複で常に3-7-7に6300円かけた場合")
        print(" 回収金：" + str(rieki))
        print(" 回収率：" + str(rieki / (ite_all*len(combi)*100)))
        print(" 的中率：" + str(ite_atari / ite_all))
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
        tn = model_name.replace('_' + Ym1 + '.sav',"")
        tn = tn.replace(dir,"")
        tn += "\n"
        for i in range(len(ll5)):
            tn += str(ll5[i])
            tn += ","
        #end
        tn += "\n"
        tn += " 3-7-7 formation (6300 yen)"
        tn += "\n"
        tn += " Recovery money : " + str(rieki)
        tn += "\n"
        tn += " Recovery rate : " + str(rieki / (ite_all*len(combi)*100))
        tn += "\n"
        tn += " hitting ratio : " + str(ite_atari / ite_all)
        tn += "\n"
        plt.title(tn, fontsize=14)
        plt.tight_layout()

        plt.savefig("rieki_sannrennpuku" + "_" + str(year) + "_" + Ym1 + "model_" + str(m) + ".png", format="png")
        # plt.savefig("rieki_sannrennpuku" + "_2022_2021model_" + str(m) + ".png", format="png")
        plt.clf()
    #end
#end

# ------------------------------------------------
# ------------------------------------------------
if __name__ == "__main__":
    main()