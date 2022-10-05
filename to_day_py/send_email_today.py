# lib
import smtplib
import glob
import numpy as np

def main(dt_now, place, nrace):
    # 馬探し
    fff = glob.glob("*today")
    fff_info = glob.glob(fff[-1] + "/*_info")
    fff_pred = glob.glob(fff[-1] + "/*_predict")
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

    # ---------------------------------
    f_email = "email_list_tmp.txt"
    with open(f_email, "r") as f:
        email_list = f.readlines()
    #end
    for l in range(len(email_list)):
        email_list[l] = email_list[l].replace("\n","")
    #end

    # -----------------------------
    MAIL_ADDRESS = "xxx@gmail.com" # e-mail adress
    PASSWORD     = "password"      # アプリパスワード
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
    Kenmei = "{}年{}月{}日{}時{}分{}秒 {}　{}R 予想".format(y,m,d,hou,min,sec, place, nrace)
    # ---------------
    Body = "3-7-7　フォーメーション \n" + \
            "-------------------------------\n" + \
            "-- 3 --------------------------\n" + \
            "-------------------------------\n"
    for i in range(3):
        Body += "{} {} \n".format(true_pred[i][0], true_pred[i][1])
    #end
    Body += "-------------------------------\n" + \
            "-- 7 --------------------------\n" + \
            "-------------------------------\n"
    for i in range(7):
        Body += "{} {} \n".format(true_pred[i+3][0], true_pred[i+3][1])
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
#end
# ------------------------------------
# ------------------------------------
if __name__ == "__main__":
    main("20220102030405", "新潟", "03")
