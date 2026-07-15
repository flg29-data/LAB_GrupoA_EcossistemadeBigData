
# Laboratório: Data Warehouse com Apache Hive no AWS EMR

Projeto desenvolvido a partir do tutorial da disciplina (eEDB-006), com o objetivo de construir um **data warehouse sobre Hadoop** utilizando o **Apache Hive** num cluster **AWS EMR**, provisionado inteiramente via Terraform. O laboratório demonstra o fluxo completo: dados brutos no S3, processamento com HiveQL sobre tabelas externas, cópia para o HDFS do cluster e persistência do resultado de volta no S3.

## Objetivos

- Provisionar infraestrutura na AWS via **Terraform**: um bucket S3 com os CSVs relacionais (clientes, produtos e vendas) e um cluster **EMR** com 2 instâncias m4.large (1 master + 1 core) com Hive instalado.
- Compreender a separação entre **dados** (arquivos no S3/HDFS) e **schema/metadados** (o Hive Metastore) — a característica schema-on-read do Hive.
- Criar tabelas em **HiveQL** distinguindo **tabelas externas** (EXTERNAL, apontando para o S3) de **tabelas gerenciadas** (MANAGED, no warehouse do HDFS).
- Executar uma consulta analítica com **JOIN**, agregação (SUM e COUNT) e ordenação, lendo os dados direto do S3.
- Reproduzir o mesmo processamento no **HDFS**, ilustrando a diferença entre armazenamento externo (S3, persistente) e local (HDFS, efêmero).
- Descomissionar toda a infraestrutura ao final.

## Arquitetura

O Terraform sobe o bucket S3 (com os dados) e o cluster EMR. O Hive lê os CSVs do S3 via tabelas externas, executa a query e grava o resultado de volta no S3. Em seguida, os dados são copiados para o HDFS e o mesmo processamento roda sobre tabelas gerenciadas, demonstrando os dois modelos de armazenamento.

## Fluxo de execução (steps do EMR)

O cluster executa 5 steps em sequência, todos concluídos com status COMPLETED:

| # | Step | O que faz |
| --- | --- | --- |
| 1 | Hive-S3-Tables | Cria tabelas externas sobre o S3, roda a query e grava o resultado no S3 |
| 2 | Copy-data-to-HDFS | Copia os CSVs do S3 para o HDFS do cluster (s3-dist-cp) |
| 3 | Hive-HDFS-Tables | Cria tabelas no HDFS, roda a mesma query e grava o resultado no HDFS |
| 4 | Copy-HDFS-results-to-S3 | Copia o resultado do HDFS de volta para o S3 |
| 5 | Show-Results | Exibe o resultado final |

## Consulta executada (HiveQL)

    INSERT OVERWRITE TABLE resultado_vendas_s3
    SELECT c.estado, p.categoria,
           round(SUM(v.quantidade * p.preco), 2) AS total_vendido,
           COUNT(*) AS num_vendas
    FROM vendas_s3 v
    JOIN clientes_s3 c ON v.id_cliente = c.id_cliente
    JOIN produtos_s3 p ON v.id_produto = p.id_produto
    GROUP BY c.estado, p.categoria
    ORDER BY total_vendido DESC;

A consulta junta vendas, clientes e produtos, agrupa por estado do cliente e categoria do produto, calcula o total vendido (quantidade × preço) e o número de vendas de cada grupo, ordenando do maior para o menor faturamento.

## Tabelas externas vs. gerenciadas

Ponto conceitual central do laboratório e a diferença prática entre os dois workflows:

| Tipo | Comando | Onde ficam os dados | Ao dar DROP TABLE |
| --- | --- | --- | --- |
| Externa (workflow S3) | CREATE EXTERNAL TABLE | Local que você aponta (S3) | O schema some, os arquivos permanecem |
| Gerenciada (workflow HDFS) | CREATE TABLE | Warehouse do Hive (HDFS) | O Hive apaga os arquivos junto |

Por isso o resultado no S3 é EXTERNAL (persiste mesmo após destruir o cluster) e no HDFS é MANAGED (efêmero, morre com o cluster).

## Resultados

O pipeline foi concluído com sucesso: os 5 steps chegaram a COMPLETED e o cluster subiu em poucos minutos. O resultado é uma tabela agregada (estado, categoria, total_vendido, num_vendas), liderada por São Paulo na categoria Eletrônicos (R$ 9.500 em 2 vendas), seguida por outros estados também com Eletrônicos no topo.

## Execução e ajustes

A execução foi realizada no terminal do AWS Academy Learner Lab (Linux), com AWS CLI e Terraform. Durante a leitura dos resultados no S3, o comando inicial com a flag --recursive falhou com a mensagem "Streaming currently is only compatible with non-recursive cp commands". A correção consistiu em ler o arquivo de resultado diretamente, sem --recursive. Após o ajuste, o resultado foi exibido corretamente e baixado para o repositório. Ao final, toda a infraestrutura foi descomissionada com terraform destroy.

## Estrutura do projeto

    aws-emr-hive-tutorial/
    ├── readme.md          # Este arquivo
    ├── TUTORIAL.md        # Tutorial original passo a passo
    ├── QUICK_TUTORIAL.md  # Versão resumida
    ├── SSH.md             # Acesso ao cluster via SSH
    ├── data/              # Dados de entrada (clientes, produtos, vendas)
    ├── terraform/         # Infraestrutura como código (bucket S3 + cluster EMR)
    ├── scripts/           # Script de descomissionamento
    ├── Images/            # Prints da execução
    └── results/           # Resultado final da consulta Hive (CSV)

## Descomissionamento

Ao final, toda a infraestrutura foi removida com terraform destroy -auto-approve, que remove o cluster EMR e o bucket S3 com todo o conteúdo. Nenhum recurso permanece ativo (execução mantida dentro do orçamento de US$ 50 do Learner Lab).

## Tecnologias utilizadas

Terraform, AWS CLI, Amazon S3, Amazon EMR, Apache Hive (HiveQL sobre Hadoop/MapReduce) e HDFS, no ambiente AWS Academy Learner Lab (região us-east-1).
EOF

mkdir -p results Images

cat > results/resultado_vendas.csv <<'EOF'
estado,categoria,total_vendido,num_vendas
SP,Eletronicos,9500.0,2
PA,Eletronicos,4500.0,1
BA,Eletronicos,4500.0,1
PR,Eletronicos,3200.0,2
RJ,Eletronicos,2500.0,1
DF,Eletronicos,2500.0,1
MG,Livros,600.0,1
CE,Acessorios,560.0,1
PE,Acessorios,450.0,1
RJ,Acessorios,430.0,2
BA,Livros,360.0,1
MG,Eletronicos,350.0,1
CE,Eletronicos,350.0,1
MA,Esportes,349.9,1
CE,Esportes,349.9,1
BA,Esportes,349.9,1
MG,Vestuario,319.8,1
GO,Acessorios,300.0,1
MS,Livros,240.0,1
RN,Vestuario,239.7,1
SP,Vestuario,239.7,1
RJ,Esportes,179.8,1
BA,Vestuario,159.9,1
DF,Vestuario,159.9,1
RS,Vestuario,159.8,1
SP,Esportes,89.9,1
AM,Esportes,89.9,1
EOF
