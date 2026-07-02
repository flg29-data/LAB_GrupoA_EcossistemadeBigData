"""
wordcount_rdd.py - WordCount com a API RDD do Spark (modelo MapReduce)
"""
import re
import shutil
import sys
from pathlib import Path

from pyspark.sql import SparkSession

# ---------------------------------------------------------------
# 0. Caminhos de entrada e saida
# ---------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent  # pasta spark-tutorial/
ARQUIVO_ENTRADA = sys.argv[1] if len(sys.argv) > 1 else str(BASE_DIR / "data" / "lorem.txt")
PASTA_SAIDA = str(BASE_DIR / "output" / "wordcount")

# Remove a saida anterior, se existir (RDD saveAsTextFile nao sobrescreve)
shutil.rmtree(PASTA_SAIDA, ignore_errors=True)

# ---------------------------------------------------------------
# 1. SparkSession + SparkContext (porta de entrada da API RDD)
# ---------------------------------------------------------------
spark = (
    SparkSession.builder
    .appName("WordCountRDD")
    .master("local[*]")
    # Fixa o driver no localhost - evita erros de rede em VPN/Wi-Fi corporativo
    .config("spark.driver.bindAddress", "127.0.0.1")
    .config("spark.driver.host", "127.0.0.1")
    .getOrCreate()
)
sc = spark.sparkContext
sc.setLogLevel("ERROR")

# ---------------------------------------------------------------
# 2. EXTRACT - le o arquivo texto como um RDD de linhas
# ---------------------------------------------------------------
linhas = sc.textFile(ARQUIVO_ENTRADA)
print(f"Arquivo de entrada : {ARQUIVO_ENTRADA}")
print(f"Total de linhas    : {linhas.count()}")

# ---------------------------------------------------------------
# 3. MAP - quebra cada linha em palavras normalizadas
# ---------------------------------------------------------------
palavras = linhas.flatMap(lambda linha: re.findall(r"[a-zA-Z]+", linha.lower()))
print(f"Total de palavras  : {palavras.count()}")

# ---------------------------------------------------------------
# 4. MAP - transforma cada palavra no par (palavra, 1)
# ---------------------------------------------------------------
pares = palavras.map(lambda palavra: (palavra, 1))

# ---------------------------------------------------------------
# 5. REDUCE - soma os 1s de cada palavra
# ---------------------------------------------------------------
contagem = pares.reduceByKey(lambda a, b: a + b)
print(f"Palavras distintas : {contagem.count()}")

# ---------------------------------------------------------------
# 6. ACAO - Top 10 palavras mais frequentes
# ---------------------------------------------------------------
top10 = contagem.takeOrdered(10, key=lambda par: -par[1])
print("\nTop 10 palavras mais frequentes:")
for posicao, (palavra, total) in enumerate(top10, start=1):
    print(f"{posicao:2d}. {palavra:<15} {total}")

# ---------------------------------------------------------------
# 7. LOAD - grava o resultado completo em disco
# ---------------------------------------------------------------
contagem.sortBy(lambda par: -par[1]).saveAsTextFile(PASTA_SAIDA)
print(f"\nResultado completo gravado em: {PASTA_SAIDA}")

spark.stop()