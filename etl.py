import pandas as pd
from sqlalchemy import create_engine, URL
import os
import logging
from datetime import datetime

# Log com arquivo salvo em disco
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('etl.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
log = logging.getLogger()

def conectar():
    url = URL.create(
        'postgresql+psycopg2',
        username='postgres',
        password='Evandro!123',
        host='localhost',
        port=5432,
        database='ecommerce'
    )
    return create_engine(url)

def extrair(caminho):
    log.info(f'Extraindo: {caminho}')
    return pd.read_csv(caminho)

def transformar(df, tabela):
    antes = len(df)
    df = df.drop_duplicates()
    df = df.dropna(how='all')
    depois = len(df)
    if antes != depois:
        log.info(f'{tabela}: {antes - depois} linhas removidas na limpeza')
    return df

def carregar(df, tabela, engine):
    df.to_sql(tabela, engine, if_exists='replace', index=False)
    log.info(f'OK - {len(df)} linhas carregadas em "{tabela}"')

def executar_etl():
    log.info('='*50)
    log.info(f'ETL iniciado: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}')
    log.info('='*50)

    engine = conectar()
    pasta = r'C:\Users\Evandro\pipeline-ecommerce'

    arquivos = {
        'olist_orders_dataset.csv': 'orders',
        'olist_order_items_dataset.csv': 'order_items',
        'olist_customers_dataset.csv': 'customers',
        'olist_products_dataset.csv': 'products',
        'olist_sellers_dataset.csv': 'sellers',
        'olist_order_payments_dataset.csv': 'payments',
        'olist_order_reviews_dataset.csv': 'reviews',
        'olist_geolocation_dataset.csv': 'geolocation',
        'product_category_name_translation.csv': 'category_translation',
    }

    sucesso = 0
    falha = 0

    for arquivo, tabela in arquivos.items():
        caminho = os.path.join(pasta, arquivo)
        try:
            df = extrair(caminho)
            df = transformar(df, tabela)
            carregar(df, tabela, engine)
            sucesso += 1
        except Exception as e:
            log.error(f'ERRO em {tabela}: {e}')
            falha += 1

    log.info('='*50)
    log.info(f'ETL concluido: {sucesso} tabelas OK, {falha} erros')
    log.info('='*50)

if __name__ == '__main__':
    executar_etl()