# lib
import smtplib
import glob
import numpy as np
import param

def send_email(dt_now, place, nrace, dname, Hassou_Time, err):
    # 馬探し
    fff_info = glob.glob(dname + "/*_info")
    fff_pred = glob.glob(dname + "/*_predict")

    if err == 0:
        temp_pred = np.loadtxt(fff_pred[0], delimiter=" ", skiprows=2, usecols=None, unpack=True, ndmin=0)
        
        # ファイル読み込み
        with open(fff_info[0].replace("_info",""), "r", encoding="utf-8") as f:
            lines = f.readlines()
        #end
    
        name = []
        for i in range(len(lines)-1):
            name.append(lines[i+1].split(",")[4])
        #end

        # 例外除去
        true_pred = []
        n = len(temp_pred[2])
        for i in range(n):
            try:
                ite = int(temp_pred[2][i] - 1)
                if name[ite] != "0":
                    true_pred.append([str(ite+1), name[ite]])
                #end
            except:
                pass
            #end
        #end

        # 数の調整
        while True:
            if len(true_pred) >= 10:
                break
            #end
            true_pred.append(["0", "0"])
        #end
    #end

    # ---------------------------------
    # mode
    mode = param.param()[3]
    if mode == 0:
        f_email = param.param()[2] # e-mail list
    else:
        f_email = param.param()[5] # e-mail list tmp
    #end

    with open(f_email, "r") as f:
        email_list = f.readlines()
    #end
    for l in range(len(email_list)):
        email_list[l] = email_list[l].replace("\n","")
    #end

    # -----------------------------
    MAIL_ADDRESS = "xxx@gmail.com" # e-mail adress
    PASSWORD     = "password"           # アプリパスワード
    # -----------------------------
    smtpobj = smtplib.SMTP('smtp.gmail.com', 587)  # SMTPサーバー名とポート番号
    smtpobj.ehlo()                                 # サーバーと接続を確立, 戻り値(250, b’smtp.gmail.com at your service)
    smtpobj.starttls()                             # TLS暗号化, 戻り値(220)
    smtpobj.login(MAIL_ADDRESS, PASSWORD)
    # -----------------------------

    """ メール作成の日本語対応するためのモジュール読込 """
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from email.header import Header
    charset = "iso-2022-jp"

    """ 以下編集が必要な部分 """
    From = MAIL_ADDRESS
    To = MAIL_ADDRESS
    # Cc = "nnn@gmail.com"
    Bcc   = email_list

    y = dt_now[0:4]
    m = dt_now[4:6]
    d = dt_now[6:8]
    hou = dt_now[8:10]
    min = dt_now[10:12]
    sec = dt_now[12:14]
    Kenmei = "{}年{}月{}日 予想".format(y,m,d)
    # ---------------
    if err == 0:    
        Body = ""
        # -----------------------
        # -----------------------
        Body += "{}年{}月{}日 {}　{}R 予想".format(y,m,d, place, nrace)
        Body += "\n"
        Body += "発走時刻 {}年{}月{}日 {}".format(y,m,d,Hassou_Time)
        Body += "\n"
        Body += "解析時刻 {}年{}月{}日{}時{}分{}秒".format(y,m,d,hou,min,sec)
        Body += "\n\n"

        # -----------------------
        # ワイド 1-5
        # 1 - 2,3,4,5,6
        # -----------------------
        Body += "-------------------------------\n"
        Body += " \n"
        Body += "ワイド 1-5　フォーメーション \n" + \
                "\n" + \
                "-- 1 --------------------------\n"
        Body += "{} {} \n".format(true_pred[0][0], true_pred[0][1])
        Body += "-- 5 --------------------------\n"                
        for i in range(1, 6):
            Body += "{} {} \n".format(true_pred[i][0], true_pred[i][1])
        #end
        Body += "-------------------------------\n"
        Body += "\n\n"

        # -----------------------
        # 馬連 1-5
        # 1 - 5,6,7,8,9
        # -----------------------
        Body += "-------------------------------\n"
        Body += " \n"
        Body += "馬連 1-5　フォーメーション \n" + \
                "\n" + \
                "-- 1 --------------------------\n"
        Body += "{} {} \n".format(true_pred[0][0], true_pred[0][1])
        Body += "-- 5 --------------------------\n"                
        for i in range(4, 9):
            Body += "{} {} \n".format(true_pred[i][0], true_pred[i][1])
        #end
        Body += "-------------------------------\n"
        Body += "\n\n"

        # -----------------------
        # 3連複 3-7-7
        # 4,5,6 - 1,2,3,7,8,9,10 - 1,2,3,7,8,9,10 
        # -----------------------
        Body += "-------------------------------\n"
        Body += "3連複 3-7-7　フォーメーション \n" + \
                "-- 3 --------------------------\n"
        for i in range(3):
            Body += "{} {} \n".format(true_pred[i+3][0], true_pred[i+3][1])
        #end
        Body += "-- 7 --------------------------\n"

        for i in range(3):
            Body += "{} {} \n".format(true_pred[i][0], true_pred[i][1])
        #end
        for i in range(4):
            Body += "{} {} \n".format(true_pred[i+6][0], true_pred[i+6][1])
        #end
        Body += "-------------------------------\n"
        Body += "\n\n"

    else:
        Body = """申し訳ございません。プログラムにエラーが生じています。
        早急に復旧に取り組みさせていただきますが、本日中の復旧は難しいかと思われます。
        ご迷惑をおかけしてしまい申し訳ございません。
        何卒よろしくお願い申し上げます。
        """

    #end
    # ---------------

    #メール本文を読み込み
    msg = MIMEMultipart()
    msg.attach(MIMEText(Body))
    msg["From"] = From
    msg["To"] = To
    msg["Subject"] = Header(Kenmei.encode(charset),charset)

    # 送信
    smtpobj.sendmail(From, [To] + Bcc, msg.as_string())
    smtpobj.quit()

    # print
    print("   send " + Kenmei)
#end
# ------------------------------------
# ------------------------------------
if __name__ == "__main__":
    send_email("20220102030405", "新潟", "03")
