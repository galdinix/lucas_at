import requests

def consultar_api_mercadolivre(jogo):
    url = f"https://api.mercadolibre.com/sites/MLB/search?category=MLB186456&q={jogo}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        resultados = []
        for result in data.get('results', []):
            nome = result.get('title', '')
            preco = result.get('price', 0)
            permalink = result.get('permalink', '')
            resultados.append((nome, preco, permalink))
        return resultados
    else:
        print(f"Erro ao consultar API para o jogo {jogo}: Status Code {response.status_code}")
        return []
    
#resultados = consultar_api_mercadolivre()
import pathlib
import sys
file = pathlib.Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))
from miniProjeto3.src.main import main

data = main()