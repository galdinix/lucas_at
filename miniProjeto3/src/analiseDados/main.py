import sys
import pathlib
import pandas as pd
from sqlalchemy.orm import Session

# Adiciona o caminho do projeto ao sys.path m

file = pathlib.Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))
from conexaoBd.database import engine, Base, get_db
from models.jogo import Jogo

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

def main():
    base_dir = pathlib.Path(__file__).resolve().parent.parent.parent.parent
    caminho_excel = base_dir / 'miniProjeto2' / 'data' / "dadosConsolidados.xlsx"

    df_excel = ler_excel(caminho_excel)
    if df_excel is None:
        return

    jogos_relacionados = extrair_jogos_relacionados(df_excel)
    lista_conjuntos_jogos = criar_lista_conjuntos_jogos(df_excel)
    jogos_unicos_set = jogos_unicos(lista_conjuntos_jogos)
    jogos_populares_set = jogos_com_mais_aparicoes(lista_conjuntos_jogos)

    dados = {
        'jogos_relacionados': jogos_relacionados,
        'jogos_unicos': jogos_unicos_set,
        'jogos_com_mais_aparicoes': jogos_populares_set
    }

    # Criar a estrutura do banco de dados
    Base.metadata.create_all(bind=engine)

    # Exportar para SQLite usando SQLAlchemy
    db = next(get_db())  # Obtém a sessão do banco de dados
    exportar_para_sqlalchemy(db, dados)

if __name__ == "__main__":
    main()

