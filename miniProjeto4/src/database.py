from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pathlib

Base = declarative_base()

def conectar_banco():
    try:
        base_dir = pathlib.Path(__file__).resolve().parent.parent.parent
        DATABASE_URL = f"sqlite:///{base_dir / 'miniProjeto4' / 'data' / 'jogo_mercado_livre.db'}"
        engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
        Session = sessionmaker(bind=engine)
        session = Session()
        return engine, session
    except Exception as ex:
        print(f'Error:{ex}')
 
def desconectar_bd(session):
    if (session):
        session.close_all()