import sys
import pathlib
import pandas as pd
from sqlalchemy.orm import Session
from database import*
from models import *

def ler_excel(caminho_arquivo):
    try:
        df = pd.read_excel(caminho_arquivo)
        return df
    except FileNotFoundError:
        print(f"Erro: Arquivo Excel não encontrado em {caminho_arquivo}")
    except pd.errors.EmptyDataError:
        print(f"Erro: Arquivo Excel vazio em {caminho_arquivo}")
    except Exception as e:
        print(f"Erro ao ler o arquivo Excel em {caminho_arquivo}: {e}")
        return None

def extrair_jogos_relacionados(df):
    try:
        jogos_relacionados = set(df['jogos_preferidos'].str.split('|').explode().tolist())
        return jogos_relacionados
    except Exception as e:
        print(f"Erro ao extrair jogos relacionados: {e}")
        return set()

def criar_lista_conjuntos_jogos(df):
    try:
        lista_conjuntos_jogos = df['jogos_preferidos'].str.split('|').apply(set).tolist()
        return lista_conjuntos_jogos
    except Exception as e:
        print(f"Erro ao criar lista de conjuntos de jogos: {e}")
        return []

def jogos_unicos(lista_conjuntos_jogos):
    try:
        todos_jogos = set.union(*lista_conjuntos_jogos)
        jogos_unicos = {jogo for jogo in todos_jogos if sum(jogo in jogos for jogos in lista_conjuntos_jogos) == 1}
        return jogos_unicos
    except Exception as e:
        print(f"Erro ao encontrar jogos únicos: {e}")
        return set()

def jogos_com_mais_aparicoes(lista_conjuntos_jogos):
    try:
        contagem_jogos = {}
        for jogos in lista_conjuntos_jogos:
            for jogo in jogos:
                contagem_jogos[jogo] = contagem_jogos.get(jogo, 0) + 1
        max_aparicoes = max(contagem_jogos.values(), default=0)
        jogos_populares = {jogo for jogo, contagem in contagem_jogos.items() if contagem == max_aparicoes}
        return jogos_populares
    except Exception as e:
        print(f"Erro ao encontrar jogos com mais aparições: {e}")
        return set()

def exportar_para_sqlalchemy(db: Session, dados):
    try:
        for tipo, jogos in dados.items():
            for jogo in jogos:
                db_jogo = Jogo(tipo=tipo, jogo=jogo)
                db.merge(db_jogo)
        db.commit()
    except Exception as e:
        print(f"Erro ao exportar para SQLite: {e}")
        db.rollback()


