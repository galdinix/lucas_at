from bs4 import BeautifulSoup
import requests
import pandas as pd
from io import StringIO
import pathlib

def limpar_colunas_dataframe(df):
    """
    Limpa e simplifica as colunas do DataFrame.

    Se as colunas forem um MultiIndex, junta os níveis em uma única string.
    Remove espaços em branco dos nomes das colunas e ajusta colunas de data de lançamento, se necessário.

    Args:
        df (pd.DataFrame): DataFrame cujas colunas precisam ser limpas.

    Returns:
        pd.DataFrame: DataFrame com as colunas limpas.
    """   
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = ['_'.join(map(str, col)).strip() for col in df.columns.values]
    else:
        df.columns = df.columns.astype(str).str.strip()
    
    df.columns = [col.replace('_Unnamed: 0_level_1', '') for col in df.columns]
    return df

def salvar_dataframe_para_csv(df, console, indice):
    """
    Salva o DataFrame em um arquivo CSV no diretório de dados.

    O arquivo é salvo no diretório "data" dentro do diretório pai do script atual.
    O nome do arquivo segue o formato "{console}_tabela{indice + 1}.csv".

    Args:
        df (pd.DataFrame): DataFrame a ser salvo.
        console (str): Nome do console para incluir no nome do arquivo.
        indice (int): Índice da tabela para incluir no nome do arquivo.
    """
    base_dir = pathlib.Path(__file__).resolve().parent.parent
    data_dir = base_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    arquivo_saida = data_dir / f"{console}_tabela{indice + 1}.csv"
    df.to_csv(arquivo_saida, index=False)

def extrair_dados(url):
    """
    Extrai dados de uma URL e retorna uma lista de DataFrames.

    Faz uma requisição HTTP para a URL fornecida, parseia o HTML retornado,
    e extrai todas as tabelas com a classe "wikitable" no formato de DataFrames do pandas.

    Args:
        url (str): URL da qual os dados serão extraídos.

    Returns:
        list[pd.DataFrame]: Lista de DataFrames contendo os dados extraídos das tabelas.
    """
    try:
        resposta = requests.get(url)
        resposta.raise_for_status()
    except requests.RequestException as e:
        print(f"Erro ao acessar {url}: {e}")
        return []

    sopa = BeautifulSoup(resposta.text, "html.parser")
    tabelas = sopa.find_all("table", {"class": "wikitable"})

    if not tabelas:
        print(f"Nenhuma tabela encontrada em {url}")
        return []

    dataframes = []
    for i, tabela_html in enumerate(tabelas):
        tabela_string = str(tabela_html)
        try:
            df = pd.read_html(StringIO(tabela_string))[0]
            df = limpar_colunas_dataframe(df)
            dataframes.append(df)
        except ValueError as e:
            print(f"Erro ao ler a tabela {i + 1} em {url}: {e}")
    
    return dataframes

def main():
    urls = {
        "playstation_5": "https://pt.wikipedia.org/wiki/Lista_de_jogos_para_PlayStation_5",
        "playstation_4": "https://pt.wikipedia.org/wiki/Lista_de_jogos_para_PlayStation_4",
        "xbox_series_x": "https://pt.wikipedia.org/wiki/Lista_de_jogos_para_Xbox_Series_X_e_Series_S",
        "xbox_360": "https://pt.wikipedia.org/wiki/Lista_de_jogos_para_Xbox_360",
        "nintendo_switch": "https://pt.wikipedia.org/wiki/Lista_de_jogos_para_Nintendo_Switch"
    }

    for console, url in urls.items():
        dataframes = extrair_dados(url)
        for indice, df in enumerate(dataframes):
            salvar_dataframe_para_csv(df, console, indice)
            print(f"Dados exportados para {console}_tabela{indice + 1}.csv")

if __name__ == "__main__":
    main()
