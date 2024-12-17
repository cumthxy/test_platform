
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    LOG_PATH = basedir + "/logs/server.log"  # 日志文件路径
    LOG_LEVEL = 'INFO'  # 日志级别
    @staticmethod
    def init_app(app):
        pass


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///mydatabase.db'


config = {
    'production': ProductionConfig,
}
