from flask import session, jsonify,url_for
from flask import Flask, request
from flask import g, current_app, jsonify, request,make_response
from app.models import TestApi
from  app.session import load_sessions
from sqlalchemy import desc
import datetime
from app import auth
from . import api
import traceback
from app.utils import utils

@api.route('/v1/test-api', methods=['POST'])
@auth.login_required
def add_test_api():
    '''登录
    :return 返回响应,保持登录状态
    '''
    name = request.json.get('name',"")
    url  = request.json.get('url',"")
    rtype = request.json.get('rtype',0)
    sessions = load_sessions()  

    if len(name)==0 or len(url)==0:
        return jsonify(re_code=401, msg='参数错误')
    sessions = load_sessions()
    test_api = TestApi()
    test_api.name = name
    test_api.url = url
    test_api.rtype = rtype
    sessions.add(test_api)
    sessions.commit()
    return jsonify(re_code=200, msg='创建成功')


@api.route('/v1/test-api', methods=['PUT'])
@auth.login_required
def update_all_test_api():
    '''登录
    :return 返回响应,保持登录状态
    '''
    id = request.json.get('id',0)
    name = request.json.get('name',"")
    url  = request.json.get('url',"")
    rtype = request.json.get('rtype',0)
    sessions = load_sessions()  
    test_api  = sessions.query(TestApi).filter(TestApi.id==id).first()
    if test_api:
        test_api.name = name
        test_api.url = url
        test_api.rtype = rtype
        sessions.commit()
    sessions.close()
    return jsonify(re_code=200, msg='修改成功')

@api.route('/v1/test-api', methods=['GET'])
@auth.login_required
def get_test_api():
    '''登录
    :return 返回响应,保持登录状态
    '''
    sessions = load_sessions()  
    test_api =  sessions.query(TestApi).order_by(desc(TestApi.id)).all()
    data = []
    for each in test_api:
        data.append(each.to_json())
    return jsonify(re_code=200, msg=data)

@api.route('/v1/test-api/<param>', methods=['GET'])
@auth.login_required
def get_test_api_by_id(param):
    '''登录
    :return 返回响应,保持登录状态
    '''
    sessions = load_sessions()  
    if param.isdigit():
        param = int(param)
        test_api  = sessions.query(TestApi).filter(TestApi.id==param).all()
    else:
        test_api  = sessions.query(TestApi).filter(TestApi.name.like(f"%{param}%")).all()
    data = []
    for each in test_api:
        data.append(each.to_json())
    return jsonify(re_code=200, msg=data)

@api.route('/v1/image-analyze', methods=['POST'])
@auth.login_required
def image_analyze():
    image = request.values.get('image',"").strip()
    test_type  = request.values.get('type',"").strip()
    name = request.values.get('name',"").strip()
    dob = request.values.get('dob',"").strip()
    pob = request.values.get('pob',"").strip()
    data = {"status": "OK","message": {
        "gender": "M",
        "idNumber": "MONY801107MTSLRR07",
        "voterId": "MLNRYR80110728M300",
        "fullName": "MOLINA NORATO YURI YERANIA",
        "fatherLastName": "MOLINA",
        "motherLastName": "NORATO",
        "name": "YURI YERANIA",
        "birthday": "15/07/1987",
        "issueYear": "2011",
        "expiryYear": "2021",
        "registrationYearAndMonth": "200101",
        "municipalNumber": "041",
        "postalCode": "87040",
        "placeNumber": "0001",
        "stateNumber": "28",
        "state": "TAMPS",
        "district": "VICTORIA",
        "subDistrict":"FRACC EL MIRADOR",
        "address": "AND 8 1121",
        "addressAll": "AND 8 1121 INF ALDAMA 87040 VICTORIA ,TAMPS.",
    }}
    return jsonify(re_code=200, msg=data)



@api.route('/v1/decrypt-md5', methods=['POST'])
@auth.login_required
def decrypt_md5():
    '''登录
    :return 返回响应,保持登录状态
    '''
    md5_type = request.json.get('md5_type',"")
    value = request.json.get('value',"")
    if len(value)==0 or len(md5_type)==0:
        return jsonify(re_code=401, msg='参数错误')
    if md5_type not in ['mx_phone','id_phone','id_ktp']:
         return jsonify(re_code=401, msg='md5_type错误')
    res = "未获取到结果"
    try:
        if md5_type =="mx_phone":
            res = utils.reverse_mxphone_md5(value)
        elif md5_type =="id_phone":
            res = utils.reverse_phone_md5(value)
        elif md5_type =="id_ktp":
            res = utils.reverse_ktp_md5(value)
        return jsonify(re_code=200, msg=res)
    except:
        res = traceback.format_exc()
        return jsonify(re_code=500, msg=res)
    

@api.route('/v1/announcement', methods=['GET'])
@auth.login_required
def get_announcement():
    '''登录
    :return 返回响应,保持登录状态
    '''
    announcement = """
    cashcash 定制特征需要手动测试
    easycash, RupiahCepat 的uname 必须写准确。
    其他用户最好也是写自己的 uname。
    字段名:id,phone,name,apply_time. 如果是md5 则 id_md5,phone_md5,mxphone_md5
    如果表中存在 id 非身份证字段，则修改为其他 类似index 等等。
    如果特别说明是北京时间，则需要apply_time_cn
    测试数据 md5需要提前校验。
    goto，图像类需要手动测试。
    whatsapp如果不是印尼需要指定国家码，国家码是两位。
    https://marketing.jctrans.com/promotion/dm/pc/dm.htm
    """
    return jsonify(re_code=200, msg=announcement)
