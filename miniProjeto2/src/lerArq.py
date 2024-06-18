import pandas as pd
import pathlib

def ler_csv(caminho_arquivo):
    try:
        df = pd.read_csv(caminho_arquivo)
        return df
    except FileNotFoundError:
        print(f"Erro: Arquivo CSV não encontrado em {caminho_arquivo}")
    except pd.errors.EmptyDataError:
        print(f"Erro: Arquivo CSV vazio em {caminho_arquivo}")
    except Exception as e:
        print(f"Erro ao ler o arquivo CSV em {caminho_arquivo}: {e}")

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

def ler_json(caminho_arquivo):
    try:
        df = pd.read_json(caminho_arquivo)
        return df
    except FileNotFoundError:
        print(f"Erro: Arquivo JSON não encontrado em {caminho_arquivo}")
    except Exception as e:
        print(f"Erro ao ler o arquivo JSON em {caminho_arquivo}: {e}")

def verificar_integridade_dos_df(df_csv, df_excel, df_json):
    if df_csv is not None:
        print("Dados do CSV:")
        print(df_csv.head())
    else:
        print("Não foi possível ler os dados do CSV.")
    
    if df_excel is not None:
        print("\nDados do Excel:")
        print(df_excel.head())
    else:
        print("Não foi possível ler os dados do Excel.")
    
    if df_json is not None:
        print("\nDados do JSON:")
        print(df_json.head())
    else:
        print("Não foi possível ler os dados do JSON.")


def main():
    """
    Função principal que chama as funções para ler os arquivos CSV, Excel e JSON e retorna os DataFrames.
    """
    base_dir = pathlib.Path(__file__).resolve().parent.parent
    caminho_csv = base_dir / 'data' / "dadosAT.csv"
    caminho_excel = base_dir / 'data' / "dadosAT.xlsx"
    caminho_json = base_dir / 'data' / "dadosAT.json"

    df_csv = ler_csv(caminho_csv)
    df_excel = ler_excel(caminho_excel)
    df_json = ler_json(caminho_json)
    verificar_integridade_dos_df(df_csv, df_excel, df_json)

    return df_csv, df_excel, df_json

if __name__ == "__main__":
    main()
