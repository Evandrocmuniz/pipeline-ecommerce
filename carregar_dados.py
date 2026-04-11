import pandas as pd
from sqlalchemy import create_engine, URL
import os, logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
log = logging.getLogger()

url = URL.create('postgresql+psycopg2', username='postgres', password='Evandro!123', host='localhost', port=5432, database='ecommerce')
engine = create_engine(url)

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

for arquivo, tabela in arquivos.items():
    caminho = os.path.join(pasta, arquivo)
    if os.path.exists(caminho):
        log.info(f'Carregando {arquivo}...')
        df = pd.read_csv(caminho)
        df.to_sql(tabela, engine, if_exists='replace', index=False)
        log.info(f'OK - {len(df)} linhas em {tabela}')
    else:
        log.warning(f'Nao encontrado: {arquivo}')

log.info('Concluido!')