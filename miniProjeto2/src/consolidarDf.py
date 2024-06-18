import pandas as pd
import limparDf
import pathlib

def consolidar_dados(dfs):
    """
    Consolida uma lista de DataFrames em um único DataFrame.

    Args:
        dfs (list of pd.DataFrame): Lista de DataFrames a serem consolidados.

    Returns:
        pd.DataFrame: DataFrame consolidado.
    """
    df_consolidado = pd.concat(dfs, ignore_index=True)
    return df_consolidado

def salvar_excel(df, caminho_arquivo):
    """
    Salva um DataFrame em um arquivo Excel.

    Args:
        df (pd.DataFrame): DataFrame a ser salvo.
        caminho_arquivo (str): Caminho para o arquivo Excel.
    """
    try:
        df.to_excel(caminho_arquivo, index=False)
        print(f"Dados consolidados salvos em {caminho_arquivo}")
    except Exception as e:
        print(f"Erro ao salvar o arquivo Excel em {caminho_arquivo}: {e}")


def main():
    df_csv, df_excel, df_json = limparDf.main()
    base_dir = pathlib.Path(__file__).resolve().parent.parent
    caminho_saida = base_dir / 'data' / "dadosConsolidados.xlsx"
    if df_csv is not None and df_excel is not None and df_json is not None:
        df_consolidado = consolidar_dados([df_csv, df_excel, df_json])
        salvar_excel(df_consolidado, caminho_saida)
        return df_consolidado

if __name__ == '__main__':
    main()