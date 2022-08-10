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

# neural_network, random forest
from sklearn import neural_network
from sklearn.ensemble import RandomForestClassifier

# lightGBM
import lightgbm as lgb

# ------------------------------------------------
# read
# ------------------------------------------------
def read_files_temp():

    # read data
    # fff_info  = glob.glob("re_data/*/*/*_info")
    # fff_result  = glob.glob("re_data/*/*/*_result")
    # maxd = 18 

    fff_info   = glob.glob("re_data/200*_data/*/*_info")
    temp = glob.glob("re_data/201*_data/*/*_info")
    fff_info   = fff_info + temp
    temp = glob.glob("re_data/2020_data/*/*_info")
    fff_info   = fff_info + temp
    fff_result = glob.glob("re_data/200*_data/*/*_result")
    temp = glob.glob("re_data/201*_data/*/*_result")
    fff_result   = fff_result + temp
    temp = glob.glob("re_data/2020_data/*/*_result")
    fff_result   = fff_result + temp

    train_info = []
    train_result = []
    for l in tqdm(range(len(fff_info))):
        try:
            temp_info   = np.loadtxt(fff_info[l],   delimiter=",", skiprows=0, usecols=None, unpack=True, ndmin=0)
            temp_result = np.loadtxt(fff_result[l], delimiter=",", skiprows=0, usecols=None, unpack=True, ndmin=0)
            
            temp_info   = temp_info.tolist()
            train_info.append(temp_info)
            temp_result = temp_result.tolist()
            train_result.append(temp_result)
        except:
            pass
    #end
    train_info = np.array(train_info)
    train_result = np.array(train_result)

    # read data
    fff_info   = glob.glob("re_data/2021_data/01/*_info")
    fff_result = glob.glob("re_data/2021_data/01/*_result")

    test_info = []
    test_result = []
    for l in range(len(fff_info)):
        temp_info   = np.loadtxt(fff_info[l],   delimiter=",", skiprows=0, usecols=None, unpack=True, ndmin=0)
        temp_result = np.loadtxt(fff_result[l], delimiter=",", skiprows=0, usecols=None, unpack=True, ndmin=0)

        temp_info   = temp_info.tolist()
        test_info.append(temp_info)
        temp_result = temp_result.tolist()
        test_result.append(temp_result[0])
    #end
    test_info = np.array(test_info)
    test_result = np.array(test_result)

    return train_info, train_result, test_info, test_result
#end

# ------------------------------------------------
# main
# ------------------------------------------------
def main():   
    print(" ------------------------------ ")
    print(" start read data")
    
    train_info, train_result, test_info, test_result = read_files_temp() 

    print(" end read data")
    print(" ------------------------------ ")

    # confirm size of array
    train_shape = train_info.shape
    test_shape = test_info.shape
    print(" ------------------------------ ")
    print(" size of train data")
    print(train_shape)
    print(" size of train data result")
    print(train_result.shape)
    print(" size of test data")
    print(test_shape)
    print(" size of test data result")
    print(test_result.shape)
    print(" ------------------------------ ")
    
    # reshape
    train_nd = train_shape[1] * train_shape[2]
    test_nd  = test_shape[1]  * test_shape[2]
    train_info = np.reshape(train_info, [train_shape[0], train_nd])
    test_info  = np.reshape(test_info,  [test_shape[0],  test_nd])

    # get the objective and explanatory variables for "train"
    objective   = train_result
    explanatory = train_info

    # get the explanatory variables for "test"
    explanatory_test = test_info

    # machine learning
    # model_name = 'neural_network_2020.sav'
    # clf = neural_network.MLPClassifier(activation="relu", alpha=0.0001)
    model_name = 'RandomForest_2021.sav'
    clf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=6)
    # model_name = 'lightgbm_2020.sav'
    # clf = lgb.LGBMClassifier()

    clf.fit(explanatory, objective)

    # モデルを保存する
    pickle.dump(clf, open(model_name, 'wb'))

    # 保存したモデルをロードする
    clf = pickle.load(open(model_name, 'rb'))
    
    # prediction
    prediction = clf.predict(explanatory_test)
    
    # accuracy
    print(" ------------------------------ ")
    print(" accuracy of train data")
    print("  " + str(clf.score(explanatory, objective)) )
    print(" accuracy of test data")
    print("  " + str(clf.score(explanatory_test, test_result)) )
    print(" ------------------------------ ")

    #print("Predicted probabilities:\n{}".format(clf.predict_proba(explanatory_test)))

    
    # analysis
    #print(explanatory_test[0][18*12])
    #print(clf.predict_proba([explanatory_test[0]]))
    #print(test_result[0])

    maxn = 16
    rieki = 0
    
    ite_acc = 0
    ite_all = 0
    for i in range(len(explanatory_test)):
        ite_recover = 0
        temp = clf.predict_proba([explanatory_test[i]])
        jlist = []

        for j in range(maxn):
            recover_rate = explanatory_test[i][18*12 + j] * temp[0][j]
            #print(recover_rate)
            #print(temp[0])

            if recover_rate > 1.0:
                ite_recover += 1
                jlist.append(j)
            #end
        #end

        if ite_recover > 0:
            for j in jlist:
                ite_all += 1
                if test_result[i] == j+1:
                    rieki += 100 * explanatory_test[i][18*12 + j]
                    if explanatory_test[i][18*12 + j] / len(jlist) > 1.0:
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



    # ana2
    maxn = 16
    rieki = 0
    st_big = 0
    censoring_max_odds = 5
    
    ite_all = 0
    for i in range(len(explanatory_test)):
        temp = clf.predict_proba([explanatory_test[i]])
        ite_all += 1
        
        be_rieki = rieki

        if test_result[i] == (temp[0].tolist()).index(max(temp[0])):
            rieki += 100 * explanatory_test[i][18*12 + int(test_result[i])-1]
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
#end

# ------------------------------------------------
# ------------------------------------------------
if __name__ == "__main__":
    main()