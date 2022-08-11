# ------------------------------------
# 数字から場所へ
# ------------------------------------
def conv_num_to_place(n):
    n = int(n)
    ret = ""
    if n == 1:
        ret = "札幌"
    elif n == 2:
        ret = "函館"
    elif n == 3:
        ret = "福島"
    elif n == 4:
        ret = "新潟"
    elif n == 5:
        ret = "東京"
    elif n == 6:
        ret = "中山"
    elif n == 7:
        ret = "中京"
    elif n == 8:
        ret = "京都"
    elif n == 9:
        ret = "阪神"
    elif n == 10:
        ret = "小倉"
    #end
    return ret
#end

# ------------------------------------
# 場所から数字へ
# ------------------------------------
def conv_place_to_num(n):
    ret = ""
    if n == "札幌":
        ret = 1
    elif n == "函館":
        ret = 2
    elif n == "福島":
        ret = 3
    elif n == "新潟":
        ret = 4
    elif n == "東京":
        ret = 5
    elif n == "中山":
        ret = 6
    elif n == "中京":
        ret = 7
    elif n == "京都":
        ret = 8
    elif n == "阪神":
        ret = 9
    elif n == "小倉":
        ret = 10
    #end
    return ret
#end
