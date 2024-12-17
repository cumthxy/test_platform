
import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer,SignatureExpired,BadSignature
from flask import jsonify, current_app, g, request
db = SQLAlchemy()






class User(db.Model):
    '''用户模型
    '''
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(255), unique=True,index=True) 
    password_hash = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime, default=datetime.datetime.now())

    @property
    def password(self):
        raise AttributeError('密码不可访问')
    @password.setter
    def password(self, password):
        '''生成hash密码'''
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        '''
        密码验证
        :param password-> 用户密码
        :return 验证成功返回True,否则返回False
        '''
        print(self.password_hash, password)
        return check_password_hash(self.password_hash, password)

    def generate_user_token(self, expiration=3600*12):
        '''
        生成确认身份的Token(密令)
        :param expiration-> 有效期限,单位为秒/此处默认设置为12h
        :return 加密过的token
        '''
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id, 'user_name': self.user_name}).decode('utf-8')

    def to_json(self):
        '''返回用户信息'''
        return {
            'user_id': self.id,
            'nickname': self.nickname,
            'email': self.email,
        }

    def __repr__(self):
        return '<User %r>' % self.nickname
    

class TestApi(db.Model):
    __tablename__ = 'test_api'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), default=1)
    url = db.Column(db.String(100), default='none')
    rtype = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now())
    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        if "create_time" in dict:
            new_time = dict['create_time'].strftime("%Y-%m-%d %H:%M:%S")
            dict['create_time']=new_time
        return dict

class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_name = db.Column(db.String(100), default="")
    file_name = db.Column(db.String(100), default="")
    uname = db.Column(db.String(100), default="")
    test_api_list = db.Column(db.String(500), default="")
    status = db.Column(db.String(100), default="待调度")
    result =  db.Column(db.String(100), default="")
    country =  db.Column(db.String(100), default="")
    is_md5 =  db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now())
    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        if "create_time" in dict:
            new_time = dict['create_time'].strftime("%Y-%m-%d %H:%M:%S")
            dict['create_time']=new_time
        return dict
    
if __name__ == "__main__":
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()