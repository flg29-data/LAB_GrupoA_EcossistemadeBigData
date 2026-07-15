# Laboratório: Data Warehouse com Apache Hive no AWS EMR

Projeto desenvolvido a partir do tutorial da disciplina (eEDB-006), com o objetivo de construir um data warehouse sobre Hadoop utilizando o Apache Hive num cluster AWS EMR, provisionado inteiramente via Terraform. O laboratório demonstra o fluxo completo: dados brutos no S3, processamento com HiveQL sobre tabelas externas, cópia para o HDFS do cluster e persistência do resultado de volta no S3.

## Objetivos

- Provisionar infraestrutura na AWS via Terraform: um bucket S3 com os CSVs relacionais (clientes, produtos e vendas) e um cluster EMR com 2 instâncias m4.large (1 master + 1 core) com Hive instalado.
- Compreender a separação entre dados (arquivos no S3/HDFS) e schema/metadados (o Hive Metastore), a característica schema-on-read do Hive.
- Criar tabelas em HiveQL distinguindo tabelas externas (EXTERNAL, apontando para o S3) de tabelas gerenciadas (MANAGED, no warehouse do HDFS).
- Executar uma consulta analítica com JOIN, agregação (SUM e COUNT) e ordenação, lendo os dados direto do S3.
- Reproduzir o mesmo processamento no HDFS, ilustrando a diferença entre armazenamento externo (S3, persistente) e local (HDFS, efêmero).
- Descomissionar toda a infraestrutura ao final.

## Arquitetura

O Terraform sobe o bucket S3 (com os dados) e o cluster EMR. O Hive lê os CSVs do S3 via tabelas externas, executa a query e grava o resultado de volta no S3. Em seguida, os dados são copiados para o HDFS e o mesmo processamento roda sobre tabelas gerenciadas, demonstrando os dois modelos de armazenamento.

## Fluxo de execução (steps do EMR)

O cluster executa 5 steps em sequência, todos concluídos com status COMPLETED:

1. Hive-S3-Tables — cria tabelas externas sobre o S3, roda a query e grava o resultado no S3
2. Copy-data-to-HDFS — copia os CSVs do S3 para o HDFS do cluster
3. Hive-HDFS-Tables — cria tabelas no HDFS, roda a mesma query e grava o resultado no HDFS
4. Copy-HDFS-results-to-S3 — copia o resultado do HDFS de volta para o S3
5. Show-Results — exibe o resultado final

## Consulta executada (HiveQL)

A consulta junta vendas, clientes e produtos, agrupa por estado do cliente e categoria do produto, calcula o total vendido (quantidade x preço) e o número de vendas de cada grupo, ordenando do maior para o menor faturamento (JOIN entre as três tabelas + SUM e COUNT + ORDER BY).

## Tabelas externas vs. gerenciadas

Ponto conceitual central do laboratório. Na tabela externa (CREATE EXTERNAL TABLE, usada no workflow S3), os dados ficam no local que você aponta e, ao dar DROP TABLE, o schema some mas os arquivos permanecem. Na tabela gerenciada (CREATE TABLE, usada no workflow HDFS), os dados ficam no warehouse do Hive e o DROP TABLE apaga os arquivos junto. Por isso o resultado no S3 é EXTERNAL (persiste após destruir o cluster) e no HDFS é MANAGED (efêmero, morre com o cluster).

## Resultados

O pipeline foi concluído com sucesso: os 5 steps chegaram a COMPLETED e o cluster subiu em poucos minutos. O resultado é uma tabela agregada (estado, categoria, total_vendido, num_vendas), liderada por São Paulo na categoria Eletrônicos (R$ 9.500 em 2 vendas), seguida por outros estados também com Eletrônicos no topo. O arquivo está em results/resultado_vendas.csv.

## Execução e ajustes

A execução foi realizada no terminal do AWS Academy Learner Lab (Linux), com AWS CLI e Terraform. Durante a leitura dos resultados no S3, o comando inicial com a flag --recursive falhou com a mensagem "Streaming currently is only compatible with non-recursive cp commands". A correção consistiu em ler o arquivo de resultado diretamente, sem --recursive. Após o ajuste, o resultado foi exibido corretamente e baixado para o repositório. Ao final, toda a infraestrutura foi descomissionada com terraform destroy.

## Descomissionamento

Ao final, toda a infraestrutura foi removida com terraform destroy -auto-approve, que remove o cluster EMR e o bucket S3 com todo o conteúdo. Nenhum recurso permanece ativo (execução mantida dentro do orçamento de US$ 50 do Learner Lab).

## Tecnologias utilizadas

Terraform, AWS CLI, Amazon S3, Amazon EMR, Apache Hive (HiveQL sobre Hadoop/MapReduce) e HDFS, no ambiente AWS Academy Learner Lab (região us-east-1).
