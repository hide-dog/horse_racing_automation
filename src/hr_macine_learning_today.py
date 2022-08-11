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
import pickle

from sklearn import preprocessing

import param

# ------------------------------------------------
# read
# ------------------------------------------------
def read_files(dname):
    # read data
    fff_info = glob.glob(dname + "/*_info")           # input
    fff_result = glob.glob(dname + "/*_result")       # result, 使用しない
    
    test_info = []
    test_result = []
    for l in range(len(fff_info)):
        temp_info   = np.loadtxt(fff_info[l],   delimiter=",", skiprows=0, usecols=None, unpack=True, ndmin=0) # 読み込み
        temp_result = np.loadtxt(fff_result[l], delimiter=",", skiprows=0, usecols=None, unpack=True, ndmin=0) # 読み込み

        temp_info = preprocessing.scale((temp_info.T).tolist()) # 規格化
        temp_info = (np.array(temp_info).T).tolist()

        # temp_info   = temp_info.tolist()
        test_info.append(temp_info)
        temp_result = temp_result.tolist()
        test_result.append(temp_result)
    #end
    test_info = np.array(test_info)
    test_result = np.array(test_result)

    return test_info, test_result, fff_info
#end

# ------------------------------------------------
# main
# ------------------------------------------------
def macine_learning(model_name, dname):   
    print(" ------------------------------ ")
    print(" start read data")
    
    test_info, test_result, fff_info = read_files(dname) 

    print(" end read data")
    print(" ------------------------------ ")

    # confirm size of array
    test_shape = test_info.shape
    print(" ------------------------------ ")
    print(" size of train data")
    print(" size of test data")
    print(test_shape)
    print(" size of test data result")
    print(test_result.shape)
    print(" ------------------------------ ")
    
    # reshape
    test_nd  = test_shape[1]  * test_shape[2]
    test_info  = np.reshape(test_info,  [test_shape[0],  test_nd])

    # get the explanatory variables for "test"
    explanatory_test = test_info

    # 保存したモデルをロードする
    model_name = param.param()[1]
    clf = pickle.load(open(model_name, 'rb'))
        
    # analysis
    time_sc = fff_info[0][0:14]
    for i in range(len(explanatory_test)):
        # list に変換
        temp = clf.predict_proba([explanatory_test[i]])
        trev = sorted(temp[0], reverse=True)
        temp = temp.tolist()
        
        # output
        with open(fff_info[i].replace("info","predict"), "w") as f:
            print(" ------------------------------ ")
            print(time_sc)
            print("rank, rate[%], Umaban")
            f.write(time_sc)
            f.write("\n")
            f.write("rank, rate[%], Umaban")
            f.write("\n")
            for j in range(len(temp[0])):
                num  = str(j+1).zfill(2)
                
                rate = "{:.2f}".format(trev[j]*100).zfill(5)

                rank = temp[0].index(trev[j])
                rank = str(rank+1).zfill(2)

                print(num + " " + rate + " " + rank)
                f.write(num + " " + rate + " " + rank)
                f.write("\n")
            #end
            print(" ------------------------------ ")
        #end
    #end
#end

# ------------------------------------------------
# ------------------------------------------------
if __name__ == "__main__":
    mname = 'lightgbm_2021.sav'
    macine_learning(mname)