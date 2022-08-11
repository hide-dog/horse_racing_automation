# --------------------------------
# parameter
# --------------------------------
time_bf    = 15                    # 発走 x 分前に解析を開始する
model_name = 'lightgbm_2021.sav'   # 学習モデル名
f_email    = "email_list_tmp.txt"  # e-mailリスト ファイル

mode       = 1                     # 実行モード, 0:通常 1:テスト用
test_id    = "202204030101"        # テストモード用のアクセス先id
# --------------------------------
# --------------------------------
def param():
    return time_bf,    \
           model_name, \
           f_email,    \
           mode,       \
           test_id
#end