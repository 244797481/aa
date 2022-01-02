# from django.shortcuts import render
from .merge import test
# Create your views here.
from django.http import JsonResponse,HttpResponse
from django.shortcuts import render
import json
from flask import request
from django.conf import settings
from .models import *
import time
import hashlib
from .crontab import scheduler
# from apscheduler.schedulers.background import BackgroundScheduler
# from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
def get_html(request):
    # return render_to_response('inputaudio.html')
    if request.method == 'POST':
        # fname = request.files['wavname']  #获取上传的文件
        fname = request.FILES.get('wavname')
        print("wavname:",fname.name)
        new_fname = '/%s/%s' % (settings.MEDIA_ROOT,fname.name)
        print("new_fname:",new_fname)
        with open(new_fname,'wb') as f:
        	for fs in fname.chunks():
        		f.write(fs)
        # return processwav(new_fname)
        return instelldb(fname.name)
    return render(request, 'inputaudio.html')

def processwav(audiopath):
	resultstr = test(audiopath)
	resultresponse={}
	resultresponse['status'] = 0 if len(resultstr) > 0 else 1
	# resultresponse['data'] = json.dumps(resultstr, ensure_ascii=False)
	resultresponse['data'] = resultstr
	print("resultresponse:",resultresponse)
	# print("resultresponse json:",json.dumps(resultresponse,ensure_ascii=False))
	instelldb(json.dumps(resultresponse,ensure_ascii=False))
	# return render_to_response('inputaudio.html',{'path_list':path_list})
	# return HttpResponse(json.dumps(resultresponse,ensure_ascii=False),content_type="application/json,charset=utf-8")

def instelldb(values):
	searchid = hashlib.md5(str(time.perf_counter()).encode('utf-8')).hexdigest()
	inputtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	asr = AsrNlpStage(inputid = searchid,createtime = inputtime,filename = values)
	asr.save()
	resultresponse={}
	resultresponse['status'] = 0
	resultresponse['filename'] = values
	resultresponse['searchid'] = searchid
	resultresponse['inputtime'] = inputtime

	ret = AsrNlpStage.objects.filter(inputid='111').all()
	# resultresponse['data'] = ret
	print("******instelldb:",instelldb)
	return HttpResponse(json.dumps(resultresponse,ensure_ascii=False),content_type="application/json,charset=utf-8")
def task_test():
    print("task_test***************************")
# def RunDaemonService():
#     print ("RunDaemonService start")
#     scheduler = BackgroundScheduler()
#     scheduler.add_jobstore(DjangoJobStore(), "default")
#     try:
#         # 监控任务
#         scheduler.add_job(task_test, 'interval', seconds=5, id='updatedb_job')
#         # 调度器开始
#         scheduler.start()
#     except Exception as e:
#         print ("RunDaemonService error:",e)
#         # 报错则调度器停止执行
#         scheduler.shutdown()
#     print ("RunDaemonService end")

def updatedb():
    # 查询出json为空的inputid 和 文件名字
    upobj = AsrNlpStage.objects.filter(resultjson__isnull=True)
    print("***upobj11:",upobj.count())
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
    print("******updatedb:")


def search(request):
    # updatedb()
    resultresponse={}
    if request.method == 'GET':
    	searid = request.GET.get('searchid','')
    	if searid:
            print("searid:",searid)
            qs = AsrNlpStage.objects.filter(inputid=searid)
            if qs.count() > 0:
                objret =  qs.first()
                resultresponse['status'] = 0
                resultresponse['searchid'] = searid
                resultresponse['filename'] = objret.filename
                resultresponse['createtime'] = objret.createtime
                resultresponse['endtime'] = objret.endtime
                resultresponse['data'] = objret.resultjson
            else:
                resultresponse['status'] = 1
                resultresponse['massage'] = 'null date'
            print("resultresponse:",resultresponse)
    return HttpResponse(json.dumps(resultresponse,ensure_ascii=False),content_type="application/json,charset=utf-8")