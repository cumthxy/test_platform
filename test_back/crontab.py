import pandas as pd
import redis
import json
from app.izi import client
import json
import os
import requests
import json
from app.utils.utils import format_ts
import copy
import time
from datetime import datetime,timedelta
from functools import partial
from concurrent.futures import ProcessPoolExecutor
import subprocess

from app.session import load_sessions
from app.models import Task
from sqlalchemy import desc
from loguru import logger
logger.add("test.log")
api_test001 = client("LxiDHIMGFpXzpLGIehps", "jXUlrGhblTtxWduqtCDMLxiDHIMGFpXzpLGIehps")

# test002需要 easycash和RupiahCepat的多头，以及 cashcash 的定制特征。这个手动做就行了，
api_test002 = client("aqGKmREhMpMojOUsBnAG", "ESbDWKJlLiSCPQTnmvTvjIxyCsRrNKyyhOnJgNOH")

def send_message(data):
    webhook = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=31da28ee-fb4c-4533-ace6-fd6f070d7b41"
    message = {
        "msgtype": "text",
        "text": {
            "content": data,
            }
        }
    message = json.dumps(message)
    requests.post(webhook, message)

def whatsapp_id(phone):
    url = "http://10.0.13.253:9302/v1/idiswadetail"
    data = {
        'number':phone,
    }
    return  json.loads(api_test001.request(url, data))


def get_whatsapp_length():
    return requests.get("https://abcdemo.xyz/iswhatsapp/status/").json("stack_length")
    

def get_api_version(uname, test_api_name):
    if uname =="":
        return "v1"
    multi_list = ['idinquiries_v1','idinquiries_v2','idinquiries_v3','idinquiries_v4',
                  'relationinquiries_v1','relationinquiries_v2',
                  'phoneinquiries_v1','phoneinquiries_v2','phoneinquiries_v3',
                  'phoneinquiries_v4'
                  ]
    test_api_name = test_api_name.split("/")[-1]+"_"+test_api_name.split("/")[-2]
    if uname =="easycash" and test_api_name in multi_list:
        print("--------------v2版本测试--------------")
        return "v2"
    if "easycash" in uname  and test_api_name in multi_list:
        print("--------------v2版本测试--------------")
        return "v2"
    #摩比神奇
    if uname =="rupiahcepat" and test_api_name in multi_list:
        print("--------------v2版本测试--------------")
        return "v2"
    if "mobi" in uname and test_api_name in multi_list:
        print("--------------v2版本测试--------------")
        return "v2"
        
    return "v1"


# 发送网络请求 保存file_name
def request_data(data, test_api_name, out_file_name, uname):
    res = "" 
    
    if "KTP" in data.get('id',"") or "phone" in data.get('phone',""):
        res = {'status': 'NOT_FOUND_MD5', 'message': "This md5 can't be found in our system"}
         
    if "idinquiries" in test_api_name and not "KTP" in data.get('id',""):
        res = "" 
    if "phoneinquiries" in test_api_name and not "phone" in data.get('phone',""):
        res = ""
    if  "phone" in data.get('phone',"") and  "KTP" not in data.get('id',"") and "blacklist" in test_api_name:
        del data['phone']
        res = ""
    if res == "":
        if get_api_version(uname, test_api_name) =="v1":
            print("--------------v1版本测试--------------")
            jsonData = api_test001.request(test_api_name, data)
        else:
            print("--------------v2版本测试--------------")
            jsonData = api_test002.request(test_api_name, data)
            
        res = json.loads(jsonData)
    if not data.get('ts',""):
        print("apply_time 时间戳不在 请确认！！！！！！！！！！！！！！！！！！！！！")
    print(res)
    result = pd.DataFrame()
    res_data = copy.deepcopy(data)
    res_data.pop('rtype', None)
    res_data.pop('number', None)
    res_data.pop('ts',None)
    res_data.pop('country',None)
    res_data.pop("callback",None)
    res_data.pop("trans",None)
    if "id_md5"  in res_data:
        res_data.pop('id',None)
    if "phone_md5"  in res_data:
        res_data.pop('phone',None)   
    if "mxphone_md5"  in res_data:
        res_data.pop('phone',None)   
    res_data['res'] = res
    
    result = result.append([res_data])
    result.to_csv(out_file_name, mode='a', header=False, index=False)
    return res

# 获取 md5结果
def reverse_ktp_md5(ktp_md5):
    url_md5 = "http://10.0.13.253:8910/v1/md5ktp"
    post_data = {"ktp": ktp_md5}
    ktpjsonData = json.loads(api_test001.request(url_md5, post_data))
    print("reverse_ktp_md5",ktpjsonData)
    ktp = ktpjsonData['message']
    return ktp

def reverse_phone_md5(phone_md5):
    url_md5 = "http://10.0.13.253:8910/v1/md5phone"
    post_data = {"phone": phone_md5 }
    phonejsonData = json.loads(api_test001.request(url_md5, post_data))
    print("reverse_phone_md5",phonejsonData)
    phone = phonejsonData['message']
    return phone

def reverse_mxphone_md5(phone_md5):
    url_md5 = "http://10.0.13.253:8910/v1/mxmd5phone"
    post_data = {"phone": phone_md5 }
    phonejsonData = json.loads(api_test001.request(url_md5, post_data))
    print("reverse_mxphone_md5",phonejsonData)
    phone = phonejsonData['message']
    return phone



def auto_insert_header(file_name, headers):
    if os.path.exists(file_name):
        out = subprocess.getoutput("sed -i '1i\{}' {}".format(headers, file_name))
        print(out)


# 提前约定好了字段，名字，并不需要判断字段类型。
def run_task(file_name, test_api_name, out_file_name, country_code = "", uname = ""):
    if file_name.endswith("csv"):
        df = pd.read_csv("static/upload/"+file_name,dtype=str)
    else:
        df = pd.read_excel("static/upload/"+file_name,dtype=str)
    column_names = df.columns.tolist() 
    if "id" in column_names:
        df['id'] =  df['id'].astype(str)
        df['id'] = df['id'].str.upper()
        df['id'] = df['id'].str.replace("'","")
    if "phone" in column_names:
        df['phone'] =  df['phone'].astype(str)
        df['phone'] = df['phone'].str.replace("'","")

    #ts回溯转换
    if "mxphone" in test_api_name or "mxid" in test_api_name:
        ts_country = "MX"
    elif "inphone" in test_api_name or 'inid' in test_api_name:
        ts_country = "IN"
    else:
        ts_country = "ID"
    if "apply_time" in column_names:
        df['ts'] = df['apply_time'].apply(lambda x: format_ts(x, ts_country ))
    elif "apply_time_cn" in column_names:
        df['ts'] = df['apply_time_cn'].apply(lambda x: format_ts(x, "CN"))
    else:
        print("apply_time 时间戳不在 请确认！！！！！！！！！！！！！！！！！！！！！")
    if "gliswadetail" in test_api_name:
        df["number"] = df['phone']
        df["country"] = country_code
    if "gliswhatsapp" in test_api_name:
        df["number"] = df['phone']
        df["country"] = country_code
        
    if "idiswadetail" in test_api_name:
        df['number'] = df['phone']
    if "idiswhatsapp" in test_api_name:
        df['number'] = df['phone']
    
        
    task_list = json.loads(df.to_json(orient='records'))

    with ProcessPoolExecutor(max_workers=3) as pool:
        partial_func = partial(request_data, test_api_name=test_api_name, out_file_name=out_file_name, uname=uname)
        pool.map(partial_func, task_list)
    new_column_names = df.columns.tolist()
    headers_to_remove = ['rtype','number','ts','country']
    if "id_md5"  in new_column_names:
        headers_to_remove.append('id')
    if "phone_md5"  in new_column_names:
        headers_to_remove.append('phone')
    if "mxphone_md5"  in new_column_names:
        headers_to_remove.append('phone')   
    headers = [x for x in new_column_names if x not in headers_to_remove]
    headers.append('res')
    headers = ",".join(headers)
    auto_insert_header(out_file_name,headers)


def run_whatsapp(file_name):
    logger.info("测试定制特征,提前跑 whatsapp")
    if file_name.endswith("csv"):
        df = pd.read_csv("static/upload/"+file_name,dtype=str)
    else:
        df = pd.read_excel("static/upload/"+file_name,dtype=str)
    for index,row in df.iterrows():
        whatsapp_id(row['phone'])
# whatsapp 的 call_back的重复 过6小时再跑一次。
# 定时获取延迟队列中的任务，如果有，那么直接执行。并且判断是不是checking,如果是那么等待10min,在请求一次。

def getmd5_result(file_name):
    if file_name.endswith("csv"):
        df = pd.read_csv("test_data/"+file_name,dtype=str)
    else:
        df = pd.read_excel("test_data/"+file_name,dtype=str)
    column_names = df.columns.tolist()
    task_list = json.loads(df.to_json(orient='records'))
    result_df = pd.DataFrame()
    if "id_md5" in column_names and "phone_md5" in column_names:
        for each in task_list:
            try:
                temp_result = copy.deepcopy(each)
                temp_result['id'] = reverse_ktp_md5(each['id_md5'])
                temp_result['phone'] = reverse_phone_md5(each['phone_md5'])
                result_df = result_df.append([temp_result])  
            except:
                pass  
    elif "id_md5" in column_names and "phone_md5" not in column_names:
        for each in task_list:
            try:
                temp_result = copy.deepcopy(each)
                temp_result['id'] = reverse_ktp_md5(each['id_md5'])
                result_df = result_df.append([temp_result])
            except:
                pass 
    elif "phone_md5" in column_names and "id_md5" not in column_names:
        for each in task_list:
            try:
                temp_result = copy.deepcopy(each)
                temp_result['phone'] = reverse_phone_md5(each['phone_md5'])
                result_df = result_df.append([temp_result])  
            except:
                pass 
    elif "mxphone_md5" in column_names and 'phone' not in column_names:
        for each in task_list:
            try:
                temp_result = copy.deepcopy(each)
                temp_result['phone'] = reverse_mxphone_md5(each['mxphone_md5'])
                result_df = result_df.append([temp_result])
            except:
                pass 
    file_name = "md5_"+file_name 
    if "csv" in file_name: 
        result_df.to_csv("test_data/"+file_name,index=False)
    else:
        result_df.to_excel("test_data/"+file_name,index=False)

def getmd5_result(file_name):
    if file_name.endswith("csv"):
        df = pd.read_csv("static/upload/"+file_name,dtype=str)
    else:
        df = pd.read_excel("static/upload/"+file_name,dtype=str)
    column_names = df.columns.tolist()
    task_list = json.loads(df.to_json(orient='records'))
    result_df = pd.DataFrame()
    if "id_md5" in column_names and "phone_md5" in column_names:
        for each in task_list:
            try:
                temp_result = copy.deepcopy(each)
                temp_result['id'] = reverse_ktp_md5(each['id_md5'])
                temp_result['phone'] = reverse_phone_md5(each['phone_md5'])
                result_df = result_df.append([temp_result])  
            except:
                pass  
    elif "id_md5" in column_names and "phone_md5" not in column_names:
        for each in task_list:
            try:
                temp_result = copy.deepcopy(each)
                temp_result['id'] = reverse_ktp_md5(each['id_md5'])
                result_df = result_df.append([temp_result])
            except:
                pass 
    elif "phone_md5" in column_names and "id_md5" not in column_names:
        for each in task_list:
            try:
                temp_result = copy.deepcopy(each)
                temp_result['phone'] = reverse_phone_md5(each['phone_md5'])
                result_df = result_df.append([temp_result])  
            except:
                pass 
    elif "mxphone_md5" in column_names and 'phone' not in column_names:
        for each in task_list:
            try:
                temp_result = copy.deepcopy(each)
                temp_result['phone'] = reverse_mxphone_md5(each['mxphone_md5'])
                result_df = result_df.append([temp_result])
            except:
                pass 
    file_name = "md5_"+file_name 
    if "csv" in file_name: 
        result_df.to_csv("static/upload/"+file_name,index=False)
    else:
        result_df.to_excel("static/upload/"+file_name,index=False)

def crontab_task():
    sessions = load_sessions()
    task  = sessions.query(Task).filter(Task.status=="待调度").order_by(desc(Task.id)).first()
    current_date = datetime.now()
    current_date_str = current_date.strftime('%Y-%m-%d')
    current_date_md_str = current_date.strftime('%m%d')
    current_date_ym_str = current_date.strftime('%Y%m')
    out_dir = uname+"_result_"+current_date_md_str
    # 新建文件夹
    result_dir = "app/static/result/{}".format(current_date_ym_str)

    output_dir = "{}/{}/".format(result_dir, out_dir)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if task:
        task.status = "执行中"
        sessions.commit()
        task_jsnon = task.to_json()
        file_name = task_jsnon['file_name']
        country = task_jsnon['country']
        uname = task_jsnon['uname']
        is_md5 = task_jsnon['is_md5']
        test_api_list = [each['url'] for each in eval(task_jsnon['test_api_list']) ]
        if is_md5==1:
            getmd5_result(file_name)
            file_name = "md5_"+file_name
        run_time_dict = {key.split("/")[-1]+"_"+key.split("/")[-2]: 0 for key in test_api_list}
        for each_test_api in test_api_list:
            each_test_api_name = each_test_api.split("/")[-1]+"_"+each_test_api.split("/")[-2]
            run_time_dict[each_test_api_name]+=1
            out_file_name  = output_dir+uname+current_date_str+"_"+each_test_api_name+"_result.csv"
            if os.path.exists(out_file_name):
                os.remove(out_file_name)
            if "creditfeature" in each_test_api_name:
                run_whatsapp(file_name)
                while True:
                    logger.info("查看 whatsapp队列长度")
                    if get_whatsapp_length()==0:
                        break
                    else:
                        time.sleep(60)
            run_task(file_name, each_test_api, out_file_name, country , uname)
            if "wadetail" in each_test_api_name or "whatsapp" in each_test_api_name:
                if run_time_dict[each_test_api_name]==1:
                    test_api_list.append(each_test_api)
                    while True:
                        logger.info("查看 whatsapp队列长度")
                        if get_whatsapp_length()==0:
                            break
                        else:
                            time.sleep(60)
        subprocess.getoutput("cd {} && tar -zcvf {}.tar.gz {}".format(result_dir, out_dir , out_dir ))
        task.status = "成功"
        sessions.commit()
    sessions.close()
crontab_task()
