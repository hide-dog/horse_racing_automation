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
from sklearn.model_selection import GridSearchCV

# lightGBM
import lightgbm as lgb
from catboost import CatBoostClassifier

from sklearn import preprocessing


year = "2021"
# year = "latest_20220810"
# ------------------------------------------------
# read
# ------------------------------------------------
def read_files_temp():

    # read data
    # fff_info  = glob.glob("re_data/*/*/*_info")
    # fff_result  = glob.glob("re_data/*/*/*_result")
    # maxd = 18 
    
    fff_info = []
    fff_result = []

    fff_info   = glob.glob("re_data/200*_data/*/*_info")
    temp = glob.glob("re_data/201*_data/*/*_info")
    fff_info   = fff_info + temp
    temp = glob.glob("re_data/2020_data/*/*_info")
    # temp = glob.glob("re_data/202*_data/*/*_info")
    fff_info   = fff_info + temp
    # temp = glob.glob("re_data/2021_data/*/*_info")
    # fff_info   = fff_info + temp
    fff_result = glob.glob("re_data/200*_data/*/*_result")
    temp = glob.glob("re_data/201*_data/*/*_result")
    fff_result   = fff_result + temp
    temp = glob.glob("re_data/2020_data/*/*_result")
    # temp = glob.glob("re_data/202*_data/*/*_result")
    fff_result   = fff_result + temp
    # temp = glob.glob("re_data/2021_data/*/*_result")
    # fff_result   = fff_result + temp

    train_info = []
    train_result = []
    for l in tqdm(range(len(fff_info))):
        try:
            temp_info   = np.loadtxt(fff_info[l],   delimiter=",", skiprows=0, usecols=None, unpack=True, ndmin=0)
            temp_result = np.loadtxt(fff_result[l], delimiter=",", skiprows=0, usecols=None, unpack=True, ndmin=0)
            
            temp_info = preprocessing.scale((temp_info.T).tolist())
            temp_info = (np.array(temp_info).T).tolist()
            
            # temp_info   = temp_info.tolist()
            train_info.append(temp_info)
            temp_result = temp_result.tolist()
            train_result.append(temp_result[0])
        except:
            pass
    #end
    train_info = np.array(train_info)
    train_result = np.array(train_result)

    # read data
    fff_info   = glob.glob("re_data/2021_data/*/*_info")
    fff_result = glob.glob("re_data/2021_data/*/*_result")
    
    redata_info = []
    test_info = []
    test_result = []
    for l in range(len(fff_info)):
        temp_info   = np.loadtxt(fff_info[l],   delimiter=",", skiprows=0, usecols=None, unpack=True, ndmin=0)
        temp_result = np.loadtxt(fff_result[l], delimiter=",", skiprows=0, usecols=None, unpack=True, ndmin=0)
        
        redata_info.append(temp_info.tolist())
        
        temp_info = preprocessing.scale((temp_info.T).tolist())
        temp_info = (np.array(temp_info).T).tolist()
        
        # temp_info   = temp_info.tolist()
        test_info.append(temp_info)
        temp_result = temp_result.tolist()
        test_result.append(temp_result[0])
    #end
    test_info = np.array(test_info)
    test_result = np.array(test_result)
    redata_info = np.array(redata_info)

    return train_info, train_result, test_info, test_result, redata_info
#end

# ------------------------------------------------
# main
# ------------------------------------------------
def main():
    
    print(" ------------------------------ ")
    print(" start read data")
    
    train_info, train_result, test_info, test_result, redata_info = read_files_temp() 

    print(" end read data")
    print(" ------------------------------ ")

    # confirm size of array
    train_shape = train_info.shape
    test_shape = test_info.shape
    redata_shape = redata_info.shape
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
    redata_nd = redata_shape[1]  * redata_shape[2]
    train_info = np.reshape(train_info, [train_shape[0], train_nd])
    test_info  = np.reshape(test_info,  [test_shape[0],  test_nd])
    redata_info  = np.reshape(redata_info,  [redata_shape[0],  redata_nd])

    # get the objective and explanatory variables for "train"
    objective   = train_result
    explanatory = train_info

    # get the explanatory variables for "test"
    explanatory_test = test_info

    model_name = 'catboost_' + year + '.sav'
    params = {'depth': [3, 5, 7],
            'learning_rate' : [0.03, 0.1, 0.15],
            'l2_leaf_reg': [1,3,7],
            'iterations': [300]
            }
    
    ctb = CatBoostClassifier(eval_metric="AUC", logging_level='Silent')
    # ctb_grid_search = GridSearchCV(ctb, params, scoring="roc_auc", cv = 3, verbose=2)
    ctb_grid_search = GridSearchCV(ctb, params, cv = 3, verbose=2)
    ctb_grid_search.fit(explanatory, objective)
    print(ctb_grid_search.best_params_)
    print(ctb_grid_search.best_index_)
    print(ctb_grid_search.best_score_)
    
    # モデルを保存する
    # clf = CatBoostClassifier(eval_metric="AUC", logging_level='Silent')
    # 2020
    # params = {'depth': [3],
    #         'learning_rate' : [0.15],
    #         'l2_leaf_reg': [3],
    #         'iterations': [300]
    #         }
    # pickle.dump(clf, open(model_name, 'wb'))

    print(" fin ")
    #end
#end

# ------------------------------------------------
# ------------------------------------------------
if __name__ == "__main__":
    main()