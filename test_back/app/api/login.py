from flask import session, jsonify,url_for
from flask import Flask, request
from flask import g, current_app, jsonify, request,make_response
from app.models import User
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer,SignatureExpired,BadSignature
from  app.session import load_sessions
import datetime
from app import auth
from . import api

@auth.verify_token
def verify_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except SignatureExpired:
        return None  # valid token, but expired
    except BadSignature:
        return None  # invalid token
    sessions = load_sessions()
    user = sessions.query(User).filter(User.id==data['id']).first()
    return user


@api.route('/v1/signin', methods=['POST'])
def signin():
    '''用户注册接口
    :return 返回注册信息{'re_code': '0', 'msg': '注册成功'}
    '''
    user_name =request.json.get('user_name')
    password =request.json.get('password')
    user = User()
    user.user_name = user_name
    user.password = password 
    sessions = load_sessions()
    try:
        sessions.add(user)
        sessions.commit()
    except Exception as e:
        current_app.logger.debug(e)
        sessions.rollback()
        return jsonify(re_code=500, msg='注册失败')
    #6.响应结果
    return jsonify(re_code=200,msg='注册成功')

@api.route('/test', methods=['POST'])
@auth.login_required
def test():
    return jsonify(re_code=200,msg='注册成功')
@api.route('/v1/login', methods=['POST'])
def login():
    '''登录
    :return 返回响应,保持登录状态
    '''
    user_name = request.json.get('user_name')
    password = request.json.get('password')
    sessions = load_sessions()  
    try:
        user = sessions.query(User).filter(User.user_name==user_name).first()
    except Exception as e:
        current_app.logger.debug(e)
        return jsonify(re_code=500, msg='查询用户失败')
    if not user:
        return jsonify(re_code=401, msg='用户不存在',user=user)
    if not user.verify_password(password):
        return jsonify(re_code=401, msg='帐户名或密码错误')

    #更新最后一次登录时间
    user.last_seen = datetime.datetime.now()
    sessions.commit()
    token = user.generate_user_token()
    return jsonify(re_code=200, msg='登录成功',token=token)





