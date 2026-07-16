# Laboratório: Hadoop Single Node com Docker e MapReduce

Projeto desenvolvido a partir do tutorial da disciplina **eEDB-006**, com o objetivo de construir um ambiente Hadoop utilizando Docker, explorando os principais componentes do ecossistema Hadoop (**HDFS, YARN e MapReduce**) em um cluster de nó único.

---

# Objetivos

- Provisionar um ambiente Hadoop Single Node utilizando Docker Compose e Docker Desktop.
- Construir uma imagem Docker personalizada contendo o Apache Hadoop 3.3.6 e todas as dependências necessárias.
- Compreender a arquitetura básica do Hadoop, incluindo NameNode, DataNode, ResourceManager e NodeManager.
- Configurar o HDFS (Hadoop Distributed File System) para armazenamento distribuído de dados.
- Executar um processamento distribuído utilizando o modelo MapReduce através da aplicação WordCount.
- Validar o funcionamento do cluster por meio das interfaces Web do NameNode e do YARN.
- Exportar o resultado do processamento para o sistema de arquivos local.

---

# Arquitetura

```text
                    Docker Desktop
                           │
                    Docker Compose
                           │
                ┌─────────────────────┐
                │ Container Hadoop    │
                │                     │
                │  NameNode           │
                │  DataNode           │
                │  ResourceManager    │
                │  NodeManager        │
                │                     │
                │        HDFS         │
                │        │            │
                │    MapReduce        │
                └────────┬────────────┘
                         │
                  result.txt (WordCount)
```

O ambiente foi executado em um único container Docker, simulando um cluster Hadoop completo. O HDFS foi utilizado como sistema de arquivos distribuído e o processamento foi realizado através do framework MapReduce utilizando o algoritmo **WordCount**.

---

# Fluxo de execução

Durante o laboratório foram realizadas as seguintes etapas:

1. Construção da imagem Docker personalizada contendo Apache Hadoop 3.3.6.
2. Inicialização do ambiente através do Docker Compose.
3. Inicialização automática dos serviços Hadoop.
4. Validação do funcionamento do cluster utilizando:
   - NameNode Web UI (porta 9870)
   - YARN ResourceManager (porta 8088)
5. Execução do algoritmo WordCount sobre um conjunto de arquivos texto.
6. Geração do arquivo final `result.txt` contendo a frequência de ocorrência das palavras.
7. Exportação do resultado para o sistema de arquivos local.

---

# Processamento realizado

O laboratório executa uma implementação personalizada do algoritmo **WordCount**, um dos exemplos clássicos de processamento distribuído utilizando MapReduce.

O processamento consiste em:

- leitura dos arquivos texto;
- divisão em palavras individuais;
- contagem das ocorrências de cada palavra;
- agregação dos resultados;
- gravação do arquivo final contendo a frequência de cada termo.

Ao final da execução foram contabilizadas:

```text
Total words counted: 1045
```

O resultado foi salvo automaticamente em:

```text
/home/hduser/wordcount/result.txt
```

Posteriormente, o arquivo foi copiado do container Docker para o computador local utilizando o comando:

```bash
docker cp hadoop:/home/hduser/wordcount/result.txt .
```

---

# Resultados

O ambiente Hadoop foi inicializado com sucesso utilizando Docker.

Os seguintes serviços permaneceram ativos durante a execução:

- NameNode
- DataNode
- ResourceManager
- NodeManager
- HDFS
- YARN

As interfaces Web foram acessadas e validadas com sucesso:

| Serviço | Porta |
|----------|------:|
| NameNode | 9870 |
| ResourceManager | 8088 |

Resultado final:

```text
Arquivo: result.txt

Total de palavras processadas: 1045
```

O processamento foi concluído com sucesso e o arquivo `result.txt` contém a frequência de ocorrência de todas as palavras encontradas no conjunto de dados utilizado no laboratório.

---

# Estrutura do projeto

```text
hadoop-docker-tutorial/
│
├── config/
│   ├── core-site.xml
│   ├── hdfs-site.xml
│   ├── ssh_config
│   └── yarn-site.xml
│
├── data/
│   └── lorem.txt
│
├── images/  --- Contém todas as evidências deste Laboratório
│
├── scripts/
│   ├── docker-entrypoint.sh
│   ├── run-custom-wordcount.sh
│   └── test-wordcount.sh
│
├── src/
│   ├── WordCountApplication.java
│   ├── WordCountMapper.java
│   └── WordCountReducer.java
│
├── Dockerfile
├── README.md
├── docker-compose.yml
└── result.txt 
```

---

# Principais comandos executados

Construção da imagem Docker:

```bash
docker compose build --no-cache
```

Inicialização do ambiente:

```bash
docker compose up -d
```

Verificação do container:

```bash
docker ps
```

Acesso ao container:

```bash
docker exec -it hadoop bash
```

Execução do WordCount:

```bash
./run-custom-wordcount.sh
```

Cópia do resultado para o computador local:

```bash
docker cp hadoop:/home/hduser/wordcount/result.txt .
```

---

# Evidências

As seguintes evidências foram coletadas durante a execução do laboratório:

- Construção da imagem Docker.
- Container Hadoop em execução (`docker ps`).
- Interface Web do NameNode.
- Interface Web do ResourceManager (YARN).
- Execução do algoritmo WordCount.
- Arquivo `result.txt` gerado com sucesso.

---

# Tecnologias utilizadas

- Docker Desktop
- Docker Compose
- Apache Hadoop 3.3.6
- HDFS (Hadoop Distributed File System)
- Apache YARN
- Apache MapReduce
- Eclipse Temurin JDK 8
- Linux (Ubuntu Focal)
- PowerShell (Windows)

---

# Conclusão

Este laboratório demonstrou a criação de um ambiente Hadoop utilizando Docker, permitindo compreender a arquitetura básica da plataforma e executar um processamento distribuído através do algoritmo WordCount.

A utilização do Docker simplificou o provisionamento do ambiente, permitindo executar todos os componentes do Hadoop em um único container, validar o funcionamento do HDFS e do YARN, além de realizar o processamento distribuído de dados utilizando MapReduce.

O projeto reproduz os principais conceitos do ecossistema Hadoop e serve como base para estudos futuros envolvendo processamento de grandes volumes de dados e aplicações Big Data.
