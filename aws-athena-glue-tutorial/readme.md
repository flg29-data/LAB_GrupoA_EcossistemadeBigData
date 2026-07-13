# Laboratório: Analytics Serverless com AWS Athena e AWS Glue

Projeto desenvolvido a partir do tutorial da disciplina (eEDB-006), com o objetivo de construir um ambiente de análise de dados **100% serverless** na AWS, sem provisionamento de clusters ou instâncias EC2.

## Objetivos

- Provisionar infraestrutura na AWS utilizando **Terraform** (Infraestrutura como Código): criação de um bucket S3 e upload de três arquivos CSV relacionais (clientes, produtos e vendas de uma loja virtual).
- Compreender a separação entre **dados** (armazenados no S3) e **schema/metadados** (armazenados no AWS Glue Data Catalog).
- Criar manualmente as tabelas `clientes`, `produtos` e `vendas` no **Glue Data Catalog** via AWS CLI, definindo colunas, tipos e formato de leitura (CSV com delimitador vírgula e cabeçalho ignorado).
- Executar uma consulta SQL no **AWS Athena** envolvendo JOIN entre as três tabelas, agregação (SUM e COUNT) e ordenação, com leitura dos dados diretamente do S3.
- Persistir o resultado da consulta como arquivo CSV no S3 e baixá-lo para o repositório.
- Descomissionar toda a infraestrutura ao final, evitando custos residuais.

## Arquitetura

```
Terraform ──▶ S3 (bucket com dados CSV e resultados)
                 ▲                    ▲
                 │ leitura dos dados  │ escrita do resultado
                 │                    │
Glue Data Catalog ◀── schema ──▶ Athena (motor de queries SQL)
```

O Glue armazena apenas os metadados (nomes de colunas, tipos e localização no S3). O Athena consulta esse catálogo para saber como interpretar os arquivos e escaneia os dados diretamente no S3, sem necessidade de carga em banco de dados intermediário.

## Consulta executada

```sql
SELECT c.estado, p.categoria,
       round(SUM(v.quantidade * p.preco), 2) AS total_vendido,
       COUNT(*) AS num_vendas
FROM athena_lab.vendas v
JOIN athena_lab.clientes c ON v.id_cliente = c.id_cliente
JOIN athena_lab.produtos p ON v.id_produto = p.id_produto
GROUP BY c.estado, p.categoria
ORDER BY total_vendido DESC;
```

A consulta junta as 30 vendas com os 15 clientes e os 10 produtos, agrupa por **estado do cliente** e **categoria do produto**, calcula o total vendido (quantidade × preço) e o número de vendas de cada grupo, ordenando do maior para o menor faturamento.

## Resultados

A execução no Athena foi concluída com status `SUCCEEDED` em poucos segundos, escaneando aproximadamente 2 KB de dados (custo ≈ $0,00, dado o modelo de cobrança de $5,00/TB escaneado).

O resultado é uma tabela agregada com as colunas `estado`, `categoria`, `total_vendido` e `num_vendas`, liderada pela categoria Eletrônicos nos estados de maior volume de compras.

### Onde estão os resultados

| Local | Descrição |
| --- | --- |
| `results/<QueryExecutionId>.csv` | Arquivo CSV com a tabela final de resultados, baixado do S3 para este repositório |
| `results/<QueryExecutionId>.csv.metadata` | Arquivo de metadados gerado automaticamente pelo Athena |
| `s3://<bucket>/results/resultado_vendas/` | Localização original no S3 (removida durante o descomissionamento) |

## Estrutura do projeto

```
aws-athena-glue-tutorial/
├── README.md          # Este arquivo
├── TUTORIAL.md        # Tutorial original passo a passo
├── data/              # Dados de entrada (clientes.csv, produtos.csv, vendas.csv)
├── terraform/         # Infraestrutura como código (bucket S3 + uploads)
├── scripts/           # Script de descomissionamento
└── results/           # Resultado final da consulta Athena (CSV)
```

## Descomissionamento

Ao final do laboratório, todos os recursos foram removidos:

1. Exclusão das tabelas e do database `athena_lab` no Glue Data Catalog (via AWS CLI).
2. `terraform destroy` para remoção do bucket S3 e de todo o seu conteúdo.

Dessa forma, nenhum recurso permanece ativo na conta, e nenhum custo recorrente é gerado.

## Tecnologias utilizadas

Terraform, AWS CLI, Amazon S3, AWS Glue Data Catalog e Amazon Athena, no ambiente AWS Academy Learner Lab (região `us-east-1`).