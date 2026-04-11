# Pipeline de Dados - E-commerce Brasileiro

Pipeline ETL completo para analise de dados do e-commerce brasileiro usando Python e PostgreSQL.

## Sobre o projeto

Projeto de portfolio de engenharia de dados que processa mais de 1.3 milhao de registros do dataset publico Olist, disponivel no Kaggle.

## Tecnologias

- Python 3.12
- PostgreSQL 18
- pandas
- SQLAlchemy
- SQL (CTEs, Window Functions, agregacoes)

## Arquitetura
### Fluxo ETL
Raw CSVs (Kaggle/Olist) → etl.py → PostgreSQL → SQL Queries → Insights

### Estrutura do Projeto
pipeline-ecommerce/
├── data/           # CSVs originais do Olist
├── etl.py          # Pipeline principal (extração, limpeza e carga)
├── queries/        # Queries SQL de análise
├── requirements.txt
└── etl.log         # Logs de execução

### Camadas

- **Extração:** Leitura dos CSVs públicos do Kaggle (dataset Olist)
- **Transformação:** Limpeza, remoção de duplicatas e normalização com pandas
- **Carga:** Inserção nas tabelas do PostgreSQL via SQLAlchemy
- **Análise:** Queries SQL com CTEs, Window Functions e agregações

## Pipeline ETL

O script etl.py realiza:
- Extracao dos CSVs originais
- Limpeza e remocao de duplicatas
- Carga nas tabelas do PostgreSQL
- Logs de execucao salvos em etl.log

## Principais insights

- Crescimento de 25x na receita entre outubro/2016 e novembro/2017
- Health and Beauty e a categoria lider com R 1.25 milhao em receita
- Watches and Gifts tem o maior ticket medio: R 201 por pedido
- Taxa de entrega varia significativamente por estado

## Como executar

1. Clone o repositorio
2. Instale as dependencias: pip install -r requirements.txt
3. Configure o PostgreSQL e crie o banco ecommerce
4. Execute: python etl.py

## Dataset

Olist Brazilian E-Commerce Dataset - disponivel em kaggle.com/datasets/olistbr/brazilian-ecommerce