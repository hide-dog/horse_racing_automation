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


# ------------------------------------------------
# main
# ------------------------------------------------
def main():   
    # ----------------------------------    
    # analysis
    # ----------------------------------
    # ----------------------------------
    # ana3
    # 当たり：if test_result[i] == (temp[0].tolist()).index(max(temp[0])):
    # オッズ：explanatory_test[i][18*12 + int(test_result[i])-1]
    # ----------------------------------
    # 一例
    # [9.4, 20.1, 2.0, 3.8, 39.7, 33.2, 172.5, 21.6, 22.9, 9.4, 14,8, 189.5, 68.8]
    # https://race.netkeiba.com/race/result.html?race_id=202203020401&rf=race_list

    odds1 = 9.4
    odds2 = 20.1
    odds3 = 2.0

    ol = np.array([9.4, 20.1, 2.0, 3.8, 39.7, 33.2, 172.5, 21.6, 22.9, 9.4, 14,8, 189.5, 68.8])
    pl = 1 / (1 + ol)
    
    # ------------------------
    # Harville(1973)            
    # ------------------------
    p1 = 1 / (1 + odds1) # rate
    p2 = 1 / (1 + odds2) # rate
    p3 = 1 / (1 + odds3) # rate
        
    # 馬単
    p = p1 * p2 / (1-p1)
    fin_odds = (p / (1-p))**-1
    if fin_odds < 1.0:
        fin_odds = 1.0
    #end
    print("馬単")
    print(fin_odds)
    
    # 三連単
    p = p1 * p2 * p3 / (1-p1) / (1-p1-p2)
    fin_odds = (p / (1-p))**-1
    if fin_odds < 1.0:
        fin_odds = 1.0
    #end
    print("3連単")
    print(fin_odds)

    # 馬連
    p = p1 * p2 / (1-p1) + p1 * p2 / (1-p2)
    fin_odds = (p / (1-p))**-1
    if fin_odds < 1.0:
        fin_odds = 1.0
    #end
    print("馬連")
    print(fin_odds)
    
    # 三連複
    p = p1 * p2 * p3 * \
        ( 1 / ((1-p1) * (1-p1-p2)) + 1 / ((1-p1) * (1-p1-p3)) + \
            1 / ((1-p2) * (1-p2-p1)) + 1 / ((1-p2) * (1-p2-p3)) + \
            1 / ((1-p3) * (1-p3-p2)) + 1 / ((1-p3) * (1-p3-p1)))
    fin_odds = (p / (1-p))**-1
    if fin_odds < 1.0:
        fin_odds = 1.0
    #end
    print("3連複")
    print(fin_odds)
    

    # 複勝
    for n in range(3):
        p = 0
        
        # 1位の確率
        p += pl[n]
        
        # 2位の確率
        for i in range(len(pl)):
            if i == n:
                continue
            #end
            p += pl[n] * pl[i] / (1-pl[i])
        #end
        
        # 3位の確率
        for i in range(len(pl)):
            for j in range(len(pl)):
                if i == j or i == n or j == n:
                    continue
                #end
                p += pl[0] * pl[i] * pl[j] / (1-pl[i])/(1-pl[i]-pl[j])
            #end
        #end

        fin_odds = (p / (1-p))**-1
        if fin_odds < 1.0:
            fin_odds = 1.0
        #end
        print("複勝" + str(n+1))
        print(fin_odds)
    #end
    
    # ワイド
    for n in range(3):
        if n == 0:
            ii = 0
            jj = 1
        elif n == 1:
            ii = 0
            jj = 2
        elif n == 2:
            ii = 1
            jj = 2
        #end
        
        p = 0
        # 1,2位の確率
        p += pl[ii] * pl[jj] / (1-pl[ii])
        # 2,1位の確率
        p += pl[jj] * pl[ii] / (1-pl[jj])
        
        for i in range(len(pl)):
            if i == ii or i == jj:
                continue
            #end
            p += pl[i] * pl[ii] * pl[jj] / (1-pl[i])/(1-pl[i]-pl[ii]) # 2,3位の確率
            p += pl[i] * pl[jj] * pl[ii] / (1-pl[i])/(1-pl[i]-pl[jj]) # 3,2位の確率
            p += pl[ii] * pl[i] * pl[jj] / (1-pl[ii])/(1-pl[ii]-pl[i]) # 1,3位の確率
            p += pl[jj] * pl[i] * pl[ii] / (1-pl[jj])/(1-pl[jj]-pl[i]) # 3,1位の確率
        #end
        
        fin_odds = (p / (1-p))**-1
        if fin_odds < 1.0:
            fin_odds = 1.0
        #end

        print("ワイド " + str(ii+1) + "," + str(jj+1) + "位")
        print(fin_odds)   
    #end 
#end

# ------------------------------------------------
# ------------------------------------------------
if __name__ == "__main__":
    main()