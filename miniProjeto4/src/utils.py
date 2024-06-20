import requests
import pandas as pd
from sqlalchemy import create_engine, inspect
import pathlib
from database import*
from models import*

def consultar_api_mercadolivre(jogo):
    try:
        url = f"https://api.mercadolibre.com/sites/MLB/search?category=MLB186456&q={jogo}"
        response = requests.get(url)
        response.raise_for_status()  # Lança uma exceção para códigos de status HTTP diferentes de 2xx
        data = response.json()
        
        resultados = []
        for result in data.get('results'):
            nome = result.get('title')
            preco = result.get('price', 0)
            permalink = result.get('permalink', '')
            resultados.append({'nome': nome, 'preco': preco, 'permalink': permalink})        
        return resultados
    except requests.exceptions.RequestException as e:
        print(f"Erro ao consultar API para o jogo {jogo}: {e}")
        return 
    except Exception as e:
        print(f"Ocorreu um erro inesperado ao consultar a API para o jogo {jogo}: {e}")
        return 
    

def obter_sql(DATABASE_URL):
    engine = create_engine(DATABASE_URL, echo=True)
    try:
        # Usar o inspector para verificar se a tabela existe
        inspector = inspect(engine)
        if not inspector.has_table('jogos'):
            print("Tabela 'jogos' não encontrada no banco de dados.")
        else:
            # Consultar todos os dados da tabela "jogos"
            query = "SELECT * FROM jogos"
            df = pd.read_sql(query, engine)
            print("Dados consultados:")
            #print(df)
            return df
    except Exception as e:
        print(f"Erro ao consultar dados: {e}")

def inserir_jogos(result, session):
    for sublist in result:
        for jogo in sublist:
            try:
                nome_jogo = jogo['nome']
                preco = jogo['preco']
                permalink = jogo['permalink']
                novo_jogo = Jogo(nome_jogo=nome_jogo, preco=preco, permaLink=permalink)
                session.add(novo_jogo)
            except KeyError as e:
                print(f"Chave não encontrada: {e}")
            except Exception as e:
                print(f"Erro ao inserir o jogo: {e}")
    try:
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Erro ao comitar as mudanças: {e}")
    desconectar_bd(session)