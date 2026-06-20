# Projeto Laboratório - Grupo A - Ecossistema de Big Data  

**Profº:** Leandro Ferreira

# Integrantes - Grupo A

- Caetano Sales Carvalho
- Fernando Luiz Gomes
- Gerson Chadi Junior
- Isabella Abreu Comelli
- Breno Tostes Garcia


## Desafio deste Laboratório

Inserir texto

Novo## Desafio deste Laboratório

O presente laboratório teve como objetivo executar um fluxo básico de processamento distribuído utilizando o ecossistema Hadoop em ambiente de nuvem, com apoio dos serviços Amazon S3 e Amazon EMR. O exercício desenvolvido consistiu na execução de uma aplicação MapReduce do tipo WordCount, responsável por processar um arquivo de texto e contabilizar a frequência de ocorrência das palavras.

A execução foi realizada em ambiente Windows 11 com WSL/Ubuntu, utilizando AWS CLI para interação com os serviços da AWS. Os arquivos de entrada e os códigos-fonte Java foram armazenados em um bucket S3. Em seguida, foi criado um cluster Amazon EMR para compilar o programa Java e executar o job MapReduce.

Durante a execução, verificou-se que o comando inicial de processamento falhou ao tentar executar o arquivo JAR diretamente a partir do caminho S3. A correção consistiu em copiar o arquivo `wordcount.jar` para o diretório local `/tmp/wordcount.jar` no nó do cluster EMR e executar o comando `hadoop jar` a partir desse arquivo local. Após o ajuste, os steps corrigidos foram concluídos com sucesso e os resultados foram gravados no S3.## Desafio deste Laboratório

O presente laboratório teve como objetivo executar um fluxo básico de processamento distribuído utilizando o ecossistema Hadoop em ambiente de nuvem, com apoio dos serviços Amazon S3 e Amazon EMR. O exercício desenvolvido consistiu na execução de uma aplicação MapReduce do tipo WordCount, responsável por processar um arquivo de texto e contabilizar a frequência de ocorrência das palavras.

A execução foi realizada em ambiente Windows 11 com WSL/Ubuntu, utilizando AWS CLI para interação com os serviços da AWS. Os arquivos de entrada e os códigos-fonte Java foram armazenados em um bucket S3. Em seguida, foi criado um cluster Amazon EMR para compilar o programa Java e executar o job MapReduce.

Durante a execução, verificou-se que o comando inicial de processamento falhou ao tentar executar o arquivo JAR diretamente a partir do caminho S3. A correção consistiu em copiar o arquivo `wordcount.jar` para o diretório local `/tmp/wordcount.jar` no nó do cluster EMR e executar o comando `hadoop jar` a partir desse arquivo local. Após o ajuste, os steps corrigidos foram concluídos com sucesso e os resultados foram gravados no S3.

## Resultados
Os principais arquivos de resultado encontram-se na pasta:

`resultados/wordcount-emr/`

Arquivos incluídos:

- `part-r-00000.txt`: saída completa do processamento WordCount;
- `top20-palavras.txt`: vinte palavras mais frequentes identificadas no arquivo de entrada;
- `steps-emr.txt`: evidência dos steps executados no Amazon EMR.

A execução final apresentou os seguintes steps concluídos com sucesso:

- `Step1-Compile-JAR`: compilação do programa Java no cluster EMR;
- `Step2-Copy-Input-S3-to-HDFS`: cópia do arquivo de entrada do S3 para o HDFS;
- `Step3-WordCount-MapReduce-Fixed`: execução corrigida do WordCount;
- `Step4-Copy-Output-HDFS-to-S3`: cópia da saída do HDFS para o S3.

## Resultados

Os principais arquivos de resultado encontram-se na pasta:

`resultados/wordcount-emr/`

Arquivos incluídos:

- `part-r-00000.txt`: saída completa do processamento WordCount;
- `top20-palavras.txt`: vinte palavras mais frequentes identificadas no arquivo de entrada;
- `steps-emr.txt`: evidência dos steps executados no Amazon EMR.

A execução final apresentou os seguintes steps concluídos com suceso:

- `Step1-Compile-JAR`: compilação do programa Java no cluster EMR;
- `Step2-Copy-Input-S3-to-HDFS`: cópia do arquivo de entrada do S3 para o HDFS;
- `Step3-WordCount-MapReduce-Fixed`: execução corrigida do WordCount;
- `Step4-Copy-Output-HDFS-to-S3`: cópia da saída do HDFS para o S3.
