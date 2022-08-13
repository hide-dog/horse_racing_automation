# --------------------------------
# --------------------------------
import sys
sys.path.append('./src') # pass
import job
# --------------------------------
# --------------------------------
import time
import schedule
import param
# --------------------------------
# --------------------------------
def main_loop():
    # 毎週土日朝にその日のスケジュールを取得、実行スケジュールの確立
    schedule.every().saturday.at("09:30").do(job.get_todays_sched)
    schedule.every().sunday.at("09:30").do(job.get_todays_sched)
    
    schedule.every(2).seconds.do(job.get_todays_sched)
    
    print(" -----------------")    
    print(" set schedule saturday.at(09:30) ")
    print(" set schedule sunday.at(09:30) ")
    print(" -----------------")

    mode = param.param()[3]
    if mode == 0:
        pass
    elif mode == 1:
        # test用
        schedule.every(2).seconds.do(job.get_todays_sched)
        print("\n")
        print(" set \"Test\" mode")
        print("\n")
    #end

    # 1秒毎にスケジュールを確認し、時間が来たら実行
    while True:
        schedule.run_pending()
        time.sleep(5)
    #end
#end
# -----------------------------------
# -----------------------------------
main_loop()