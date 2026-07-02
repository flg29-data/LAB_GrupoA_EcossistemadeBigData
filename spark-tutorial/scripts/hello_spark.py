"""
hello_spark.py - Primeiro programa com Apache Spark
Cria uma SparkSession, monta um DataFrame minusculo e mostra na tela.
Se este script rodar, seu ambiente Spark esta funcionando.
"""
from pyspark.sql import SparkSession

# 1. Cria (ou reaproveita) a sessao Spark - porta de entrada de tudo no Spark
spark = (
    SparkSession.builder
    .appName("HelloSpark")
    .master("local[*]")  # roda local, usando todos os nucleos da maquina
    # Fixa o driver no localhost - evita erros de rede em VPN/Wi-Fi corporativo
    .config("spark.driver.bindAddress", "127.0.0.1")
    .config("spark.driver.host", "127.0.0.1")
    .getOrCreate()
)

# 2. Reduz o volume de logs para enxergar melhor a saida
spark.sparkContext.setLogLevel("ERROR")

print("=" * 50)
print("Hello, Spark!")
print(f"Versao do Spark : {spark.version}")
print(f"Master          : {spark.sparkContext.master}")
print("=" * 50)

# 3. Cria um DataFrame de teste com 3 linhas
dados = [("Ana", 28), ("Bruno", 34), ("Carla", 25)]
df = spark.createDataFrame(dados, ["nome", "idade"])

# 4. Acoes: show() imprime a tabela, count() conta as linhas
df.show()
print(f"Total de linhas: {df.count()}")

# 5. Encerra a sessao
spark.stop()
print("Sessao encerrada com sucesso. Ambiente OK!")