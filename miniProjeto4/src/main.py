import pathlib
import sys
import requests
from processarDados import*
from utils import*
from database import*
import time
from models import*
file = pathlib.Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))


    
def main():
    base_dir = pathlib.Path(__file__).resolve().parent.parent.parent
    DATABASE_URL = f"sqlite:///{base_dir / 'miniProjeto3' / 'data' / 'jogos.db'}"
    df_jogos = obter_sql(DATABASE_URL)
    result = []
    print("aguardando consulta a api")
    for item in df_jogos['jogo']:
        result.append(consultar_api_mercadolivre(item))
        #time.sleep(0.3)
    print('consulta realizada com sucesso!!!')
    engine, session = conectar_banco()
    Base.metadata.create_all(engine)
    inserir_jogos(result, session)


    
        
       
main()