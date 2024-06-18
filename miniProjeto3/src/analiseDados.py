import pathlib
import pandas as pd
import sqlite3

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

def obter_jogos_relacionados(df):
    if df is None:
        print("Erro: DataFrame está vazio ou não foi carregado corretamente.")
        return [], [], []

    if 'jogos_preferidos' not in df.columns:
        print("Erro: Coluna 'jogos_preferidos' não encontrada no DataFrame.")
        return [], [], []

    # Extrair todos os jogos relatados
    jogos_relacionados = df['jogos_preferidos'].str.split('|').explode().unique().tolist()
    
    # Converter cada linha do DataFrame em um conjunto de jogos
    lista_conjuntos_jogos = df['jogos_preferidos'].str.split('|').apply(set).tolist()
    
    # Jogos relatados por apenas um usuário
    jogos_unicos = set(jogo for jogos in lista_conjuntos_jogos for jogo in jogos if sum(jogo in jogos_conjuntos for jogos_conjuntos in lista_conjuntos_jogos) == 1)
    
    # Contagem de aparições de cada jogo
    contagem_jogos = {}
    for jogos in lista_conjuntos_jogos:
        for jogo in jogos:
            if jogo in contagem_jogos:
                contagem_jogos[jogo] += 1
            else:
                contagem_jogos[jogo] = 1
    
    # Jogos com mais aparições
    jogos_com_mais_aparicoes = [jogo for jogo, contagem in contagem_jogos.items() if contagem == max(contagem_jogos.values())]
    
    return jogos_relacionados, list(jogos_unicos), jogos_com_mais_aparicoes

def exportar_para_sqlite(db_path, dados):
    # Conectar ao banco de dados SQLite
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Criar tabela se não existir
    c.execute('''CREATE TABLE IF NOT EXISTS jogos (
                    tipo TEXT,
                    jogo TEXT
                )''')
    
    # Inserir dados
    for tipo, jogos in dados.items():
        for jogo in jogos:
            c.execute("INSERT INTO jogos (tipo, jogo) VALUES (?, ?)", (tipo, jogo))
    
    # Salvar (commit) as mudanças e fechar a conexão
    conn.commit()
    conn.close()

def main():
    base_dir = pathlib.Path(__file__).resolve().parent.parent.parent
    caminho_excel = base_dir / 'miniProjeto2' / 'data' / "dadosConsolidados.xlsx"
    db_path = base_dir / 'miniProjeto3' / 'data' / 'jogos.db'

    # Ler o arquivo Excel
    df_excel = ler_excel(caminho_excel)
    
    # Realizar operações com conjuntos
    jogos_relacionados, jogos_unicos, jogos_com_mais_aparicoes = obter_jogos_relacionados(df_excel)
    
    # Organizar os dados para exportação
    dados = {
        'jogos_relacionados': jogos_relacionados,
        'jogos_unicos': jogos_unicos,
        'jogos_com_mais_aparicoes': jogos_com_mais_aparicoes
    }
    
    # Exportar para SQLite
    exportar_para_sqlite(db_path, dados)

if __name__ == "__main__":
    main()
