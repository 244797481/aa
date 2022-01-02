import time
from django.conf import settings
from apscheduler.schedulers.background import BackgroundScheduler
from .models import *
from .merge import test
def job_func():
    print ("RunDaemonService update db start")
    # 查询出json为空的inputid 和 文件名字
    upobj = AsrNlpStage.objects.filter(resultjson__isnull=True)
    print("***需要处理的count:",upobj.count())
    if upobj.count() >= 1:
       for item in upobj:
           print("***upobj11:",item.inputid)
           print("***upobjfilename:",item.filename)
           # 文件名字执行test
           db_fname = '/%s/%s' % (settings.MEDIA_ROOT,item.filename)
           print("***db_fname:",db_fname)
           # 组织数据保存到db
           resultstr = test(db_fname)
           print("***resultstr:",resultstr)
           # result={}
           # result['data'] = resultstr
           aobj = AsrNlpStage.objects.filter(inputid=item.inputid).first()
           # aobj=asrnlpstage_obj
           print("***asrnlpstage_obj:",aobj.createtime)
           aobj.endtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
           # aobj.resultjson= json.dumps(result,ensure_ascii=False)
           aobj.resultjson= resultstr
           aobj.save()
    print ("RunDaemonService update db end")

scheduler = BackgroundScheduler()

# 每小时触发一次job_func;
# scheduler.add_job(job_func, 'date', run_date='2019-08-11 16:00:20')

# 带有起止时间的interval;
# scheduler.add_job(job_func, 'interval', minutes=0.1, start_date='2019-08-11 16:02:20', end_date='2019-08-11 16:02:40')

# 截止到2019年12月31日前，每个周一到周四，每分钟的0秒时刻，执行一次job_func;
# scheduler.add_job(job_func, 'cron', day_of_week='0-4', hour='8-16', minute='0-59', second='0', end_date='2019-12-31')

# scheduler.start()
try:
   # 每隔1分钟执行一次 job_func;
   scheduler .add_job(job_func, 'interval', seconds=60)
   # 调度器开始
   scheduler.start()
except Exception as e:
   print ("RunDaemonService error:",e)
        # 报错则调度器停止执行
   scheduler.shutdown()
print ("RunDaemonService end")