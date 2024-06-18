from utils import*
import pathlib

def main():
    base_dir = pathlib.Path(__file__).resolve().parent.parent.parent
    caminho_excel = base_dir / 'miniProjeto2' / 'data' / "dadosConsolidados.xlsx"

    #df_excel = ler_excel(caminho_excel)
    df_excel = pd.read_excel(caminho_excel)
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
    return dados

if __name__ == "__main__":
    main()
