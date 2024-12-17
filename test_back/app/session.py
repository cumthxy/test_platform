from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from config import ProductionConfig

def load_sessions():
    ENGINE = create_engine(ProductionConfig.SQLALCHEMY_DATABASE_URI,connect_args={"check_same_thread": False})
    Session = sessionmaker(bind=ENGINE, autocommit=False, autoflush=False)
    session = Session()
    return session


