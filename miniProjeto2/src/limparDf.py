import pandas as pd
import pathlib
import json
import lerArq

def limpar_dados(df):
    if df is None:
        return None

    df = df.drop_duplicates()
    df['data_nascimento'] = pd.to_datetime(df['data_nascimento'], errors='coerce')
    df = df.dropna(subset=['data_nascimento'])
    df['email'] = df['email'].apply(lambda x: x if '@' in x else None)
    df = df.dropna(subset=['email'])
    df['consoles'] = df['consoles'].fillna('')

    return df

def verificar_dfs(df, tipo_arq):
    
    if df is not None:
        print(f'Dados do {tipo_arq} (depois da limpeza):')
        print(f'{df.head()}')
        return
    print(f'Erro ao carregar CSV do tipo {tipo_arq}.')

def main():
    df_csv, df_excel, df_json = lerArq.main()
    df_csv = limpar_dados(df_csv)
    df_excel = limpar_dados(df_excel)
    df_json = limpar_dados(df_json)

    verificar_dfs(df_csv, 'csv')  
    verificar_dfs(df_excel, 'excel')
    verificar_dfs(df_json, 'json')

    return df_csv, df_excel, df_json

if __name__ == "__main__":
    main()
