from flask import session, jsonify,url_for
from flask import Flask, request,send_file
from flask import g, current_app, jsonify, request,make_response
from app.models import Task
from  app.session import load_sessions
from sqlalchemy import desc,and_
import datetime
import os 
import json 
import re
import pandas as pd 
from app import auth
from . import api

def check_file(file_name):
    try:
        if file_name.endswith("csv"):
            df = pd.read_csv(file_name,dtype=str)
        else:
            df = pd.read_excel(file_name,dtype=str)
        column_names = df.columns.tolist()            
        if "id" in column_names:
            if len(df['id'].values[0])==32:
                return False, "id字段是md5,修改列名，请重新检查后上传"
            
        if "phone" in column_names:
            if len(df['phone'].values[0])==32:
                return False, "phone字段是md5,修改列名，请重新检查后上传"
        res_list = []
        if not "id" in column_names and not "id_md5" in column_names:
            res_list.append("id列不存在")
        if not "phone" in column_names and not "phone_md5" in column_names and not "mxphone_md5" in column_names:
            res_list.append("phone列不存在")
        if not "apply_time" in column_names and not "apply_time_cn" in column_names:
            res_list.append("apply_time列不存在")
        return True, ",".join(res_list)
    except:
        return False, "文件有密码，解密之后复制到一个无密的文件中重新上传！！！！"
    

@api.route('/v1/test-task', methods=['POST'])
@auth.login_required
def add_test_task():
    '''登录
    :return 返回响应,保持登录状态
    '''
    file = request.files.get('file')
    if file:
        file_name = file.filename
        file.save(os.path.join("app/static/upload", file_name))
        if not ("csv" in file_name or "xls" in file_name):
            return jsonify(re_code=500, msg='文件格式不支持')
        check_status, check_message = check_file(os.path.join("app/static/upload", file_name))
        print(check_status, check_message)
        if not check_status:
            return jsonify(re_code=500, msg=check_message)
    else:
        return jsonify(re_code=500, msg="请上传文件")
    
    task_name = request.values.get('task_name',"").strip()
    country = request.values.get('country',"").strip()
    if len(task_name)==0:
        return jsonify(re_code=500, msg="请写task_name")
    uname  = request.values.get('uname',"").strip()
    if len(uname)==0:
        return jsonify(re_code=500, msg="请写uname")
    is_md5  = request.values.get('is_md5',0)
    
    test_api_list = request.values.get('test_api_list',"").strip()
    print("test_api_list",test_api_list)
    test_url_list  = list(set([each['url'].split("/")[-1] for each in  eval(test_api_list)]))
    if "creditfeature" in test_url_list and (re.search("id列不存在|phone列不存在|apply_time列不存在",check_message)):
        return jsonify(re_code=500, msg="id 列或者 phone列不存在或者apply_time列不存在")
    if "idinquiries" in test_url_list  and (re.search("id列不存在|apply_time列不存在",check_message)):
        return jsonify(re_code=500, msg="id 列或apply_time列不存在")
    if "phoneinquiries" in test_url_list and (re.search("phone列不存在|apply_time列不存在",check_message)):
        return jsonify(re_code=500, msg="phone 列或apply_time列不存在")
    if "relationinquiries" in test_url_list and (re.search("id列不存在|apply_time列不存在",check_message)):
        return jsonify(re_code=500, msg="id 列或apply_time列不存在")
    
    if "creditscore" in test_url_list and (re.search("id列不存在|phone列不存在|apply_time列不存在",check_message)):
        return jsonify(re_code=500, msg="id 列或者 phone列不存在或者apply_time列不存在")
    
    if "blacklist" in test_url_list and (re.search("id列不存在|apply_time列不存在",check_message)):
        return jsonify(re_code=500, msg="id 列或apply_time列不存在")
    if "fraud" in test_url_list and (re.search("id列不存在|phone列不存在|apply_time列不存在",check_message)):
        return jsonify(re_code=500, msg="id 列或者 phone列不存在或者apply_time列不存在")
    if "reconnection" in test_url_list and (re.search("id列不存在|phone列不存在",check_message)):
         return jsonify(re_code=500, msg="id 列或者 phone列不存在")
    if "identitycheck" in test_url_list and (re.search("id列不存在",check_message)):
        return jsonify(re_code=500, msg="id 列或者 phone列不存在")
    if "phonescore" in  test_url_list and (re.search("phone列不存在|apply_time列不存在",check_message)):
        return jsonify(re_code=500, msg="phone列不存在或者apply_time列不存在")
    if "phoneage" in  test_url_list and (re.search("phone列不存在|apply_time列不存在",check_message)):
        return jsonify(re_code=500, msg="phone列不存在或者apply_time列不存在")
    if "phoneverify" in  test_url_list and (re.search("id列不存在|phone列不存在",check_message)):
        return jsonify(re_code=500, msg="id 列或者 phone列不存在")
    if "topup" in  test_url_list and (re.search("phone列不存在|apply_time列不存在",check_message)):
         return jsonify(re_code=500, msg="phone列不存在或者apply_time列不存在")
    if "preference" in  test_url_list and (re.search("phone列不存在",check_message)):
        return jsonify(re_code=500, msg="phone列不存在")
    if "bpjs" in  test_url_list and (re.search("id列不存在",check_message)):
        return jsonify(re_code=500, msg="id列不存在")
    if "salary" in  test_url_list and (re.search("id列不存在",check_message)):
        return jsonify(re_code=500, msg="id列不存在")

    if len(test_url_list)==0:
        return jsonify(re_code=500, msg="请写选择接口")
    sessions = load_sessions()  
    test_task = Task()
    test_task.task_name = task_name
    test_task.uname = uname
    test_task.is_md5 = is_md5
    test_task.status = "待调度"
    test_task.test_api_list = test_api_list
    test_task.file_name = file_name
    test_task.country = country
    sessions.add(test_task)
    sessions.commit()
    return jsonify(re_code=200, msg='创建成功')


@api.route('/v1/test-task', methods=['PUT'])
@auth.login_required
def update_test_task():
    '''登录
    :return 返回响应,保持登录状态
    '''
    file = request.files.get('file')
    if file:
        file_name = file.filename
        file.save(os.path.join("app/static/upload", file_name))
        if not ("csv" in file_name or "xls" in file_name):
            return jsonify(re_code=500, msg='文件格式不支持')
        check_status, check_message = check_file(os.path.join("app/static/upload", file_name))
        if not check_status:
            return jsonify(re_code=500, msg=check_message)
    else:
        file_name = ""
    task_name = request.values.get('task_name',"").strip()
    id = request.values.get('id',"").strip()
    if not id:
         return jsonify(re_code=500, msg="参数错误，必须传 id")
    uname  = request.values.get('uname',"").strip()
    if not uname:
        return jsonify(re_code=500, msg="参数错误，必须传 uname")
    test_api_list = request.values.get('test_api_list',"").strip()
    if not test_api_list:
        return jsonify(re_code=500, msg="参数错误，必须传 测试接口")
    is_md5 =  request.values.get('is_md5',0)
    country = request.values.get('country',"").strip()
    test_url_list  = list(set([each['url'].split("/")[-1] for each in  eval(test_api_list)]))
    if "creditfeature" in test_url_list and (re.search("id列不存在|phone列不存在|apply_time列不存在",check_message)):
        return jsonify(re_code=500, msg="id 列或者 phone列不存在或者apply_time列不存在")
    if "idinquiries" in test_url_list  and (re.search("id列不存在|apply_time列不存在",check_message)):
        return jsonify(re_code=500, msg="id 列或apply_time列不存在")
    if "phoneinquiries" in test_url_list and (re.search("phone列不存在|apply_time列不存在",check_message)):
        return jsonify(re_code=500, msg="phone 列或apply_time列不存在")
    if "relationinquiries" in test_url_list and (re.search("id列不存在|apply_time列不存在",check_message)):
        return jsonify(re_code=500, msg="id 列或apply_time列不存在")
    
    if "creditscore" in test_url_list and (re.search("id列不存在|phone列不存在|apply_time列不存在",check_message)):
        return jsonify(re_code=500, msg="id 列或者 phone列不存在或者apply_time列不存在")
    
    if "blacklist" in test_url_list and (re.search("id列不存在|apply_time列不存在",check_message)):
        return jsonify(re_code=500, msg="id 列或apply_time列不存在")
    if "fraud" in test_url_list and (re.search("id列不存在|phone列不存在|apply_time列不存在",check_message)):
        return jsonify(re_code=500, msg="id 列或者 phone列不存在或者apply_time列不存在")
    if "reconnection" in test_url_list and (re.search("id列不存在|phone列不存在",check_message)):
         return jsonify(re_code=500, msg="id 列或者 phone列不存在")
    if "identitycheck" in test_url_list and (re.search("id列不存在",check_message)):
        return jsonify(re_code=500, msg="id 列或者 phone列不存在")
    if "phonescore" in  test_url_list and (re.search("phone列不存在|apply_time列不存在",check_message)):
        return jsonify(re_code=500, msg="phone列不存在或者apply_time列不存在")
    if "phoneage" in  test_url_list and (re.search("phone列不存在|apply_time列不存在",check_message)):
        return jsonify(re_code=500, msg="phone列不存在或者apply_time列不存在")
    if "phoneverify" in  test_url_list and (re.search("id列不存在|phone列不存在",check_message)):
        return jsonify(re_code=500, msg="id 列或者 phone列不存在")
    if "topup" in  test_url_list and (re.search("phone列不存在|apply_time列不存在",check_message)):
         return jsonify(re_code=500, msg="phone列不存在或者apply_time列不存在")
    if "preference" in  test_url_list and (re.search("phone列不存在",check_message)):
        return jsonify(re_code=500, msg="phone列不存在")
    if "bpjs" in  test_url_list and (re.search("id列不存在",check_message)):
        return jsonify(re_code=500, msg="id列不存在")
    if "salary" in  test_url_list and (re.search("id列不存在",check_message)):
        return jsonify(re_code=500, msg="id列不存在")
    sessions = load_sessions()  
    test_task  = sessions.query(Task).filter(Task.id==id).first()
    if test_task:
        if test_task.status != "待调度":
            return jsonify(re_code=500, msg='任务无法修改')
        test_task.uname = uname
        test_task.is_md5 = is_md5
        test_task.test_api_list = test_api_list
        test_task.task_name = task_name
        test_task.country = country
        if len(file_name)>0:
            test_task.file_name = file_name
        sessions.commit()
    sessions.close()
    return jsonify(re_code=200, msg='修改成功')


@api.route('/v1/test-task', methods=['DELETE'])
@auth.login_required
def delet_test_task():
    '''登录
    :return 返回响应,保持登录状态
    '''
    id = request.values.get('id',"").strip()
    if not id:
         return jsonify(re_code=500, msg="参数错误，必须传 id")
    
    sessions = load_sessions()  
    test_task  = sessions.query(Task).filter(Task.id==int(id)).first()
    if test_task:
        if test_task.status != "待调度":
            return jsonify(re_code=500, msg='任务无法删除')
        sessions.delete(test_task)
        sessions.commit()
    sessions.close()
    return jsonify(re_code=200, msg='删除成功')

@api.route('/v1/test-task', methods=['GET'])
@auth.login_required
def get_test_task():
    '''登录
    :return 返回响应,保持登录状态
    '''
    id = request.values.get('id',"").strip()
    status  = request.values.get('status',"").strip()
    task_name = request.values.get('task_name',"").strip()
    uname = request.values.get('uname',"").strip()
    sessions = load_sessions()  
    query = sessions.query(Task)
    filters = []
    if id:
        filters.append(Task.id==int(id))
    if status:
        filters.append(Task.status==status)
    if task_name:
        filters.append(Task.task_name.like(f"%{task_name}%"))
    if uname:
        filters.append(Task.uname.like(f"%{uname}%"))
    if filters:
        query = query.filter(and_(*filters))
    data = []
    result = query.order_by(desc(Task.id)).all()
    for each in result:
        data.append(each.to_json())
    return jsonify(re_code=200, msg=data)

@api.route('/v1/test-task/download', methods=["GET"])
@auth.login_required
def download_result():
    id = request.values.get('id',"").strip()
    if not id:
         return jsonify(re_code=500, msg="参数错误，必须传 id")
    sessions = load_sessions()  
    test_task  = sessions.query(Task).filter(Task.id==int(id)).first()
    if test_task:
        if test_task.status != "成功":
            return jsonify(re_code=500, msg='无测试结果')
        else:
            result_name = test_task.result
            if len(result_name)=="":
                return jsonify(re_code=500, msg='无测试结果稍后重试')
            file_name =os.path.join("static/result", test_task.result )   
    sessions.close()
    return send_file(file_name,attachment_filename=result_name, as_attachment=True)
