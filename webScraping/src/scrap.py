import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time


driver = webdriver.Chrome()
url = 'https://pt.wikipedia.org/wiki/Lista_de_jogos_para_PlayStation_5'
driver.get(url)
time.sleep(5)
response  = driver.page_source
print(response)
if response.status_code == 200:
    soup = BeautifulSoup(response, 'html.parser')
    # Encontrando a tabela de jogos
    table = soup.find('table', class_='wikitable')

    # Verificando se encontramos a tabela
    if table:
        # Iterando pelas linhas da tabela
        for row in table.find_all('tr'):
            # Obtendo as células de cada linha
            cells = row.find_all(['th', 'td'])
            if cells:
                # Extraindo o conteúdo de cada célula
                cell_data = [cell.get_text(strip=True) for cell in cells]
                print(cell_data)  # Aqui você pode processar os dados conforme necessário
    else:
        print("Tabela não encontrada na página.")
else:
    print("Falha ao baixar a página.")

driver.quit()

def main():
    return