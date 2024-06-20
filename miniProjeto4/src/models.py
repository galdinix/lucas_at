from database import*
from sqlalchemy import Column, String, Float, Integer

class Jogo(Base):
    __tablename__='jogo_mercado_livre'

    id_jogo = Column(Integer, primary_key=True)
    nome_jogo = Column(String)
    preco = Column(Float)
    permaLink = Column(String)