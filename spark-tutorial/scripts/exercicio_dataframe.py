from pathlib import Path
from pyspark.sql import SparkSession, functions as F

BASE_DIR = Path(__file__).resolve().parent.parent
ARQUIVO_JCR = str(BASE_DIR / "data" / "jcr.csv")
ARQUIVO_SCIMAGO = str(BASE_DIR / "data" / "scimago.csv")
SAIDA_PARQUET = str(BASE_DIR / "output" / "periodicos_parquet")
SAIDA_CSV = str(BASE_DIR / "output" / "periodicos_csv")

spark = (
    SparkSession.builder
    .appName("ExercicioDataFrame")
    .master("local[*]")
    .config("spark.driver.bindAddress", "127.0.0.1")
    .config("spark.driver.host", "127.0.0.1")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("ERROR")

def padronizar(df):
    return (
        df
        .withColumnRenamed("Rank", "rank")
        .withColumnRenamed("Full Journal Title", "titulo")
        .withColumnRenamed("Abbreviated Title", "titulo_abreviado")
        .withColumnRenamed("ISSN", "issn")
        .withColumnRenamed("Total Cites", "total_citacoes")
        .withColumnRenamed("Journal Impact Factor", "fator_impacto")
        .withColumn("issn", F.trim(F.col("issn")))
        .withColumn("total_citacoes", F.col("total_citacoes").cast("int"))
        .withColumn("fator_impacto", F.col("fator_impacto").cast("double"))
    )

df_jcr = padronizar(spark.read.csv(ARQUIVO_JCR, header=True, inferSchema=True))
df_scimago = padronizar(spark.read.csv(ARQUIVO_SCIMAGO, header=True, inferSchema=True))

print(f"Linhas JCR     : {df_jcr.count()}")
print(f"Linhas Scimago : {df_scimago.count()}")

nulos = df_scimago.filter(F.col("fator_impacto").isNull()).count()
print(f"Linhas sem fator de impacto no Scimago: {nulos}")

df_scimago = df_scimago.dropna(subset=["fator_impacto"])
print(f"Linhas Scimago apos limpeza: {df_scimago.count()}")

df_uniao = (
    df_jcr.withColumn("fonte", F.lit("jcr"))
    .unionByName(df_scimago.withColumn("fonte", F.lit("scimago")))
)
print(f"Linhas apos union (jcr + scimago): {df_uniao.count()}")

df_uniao.groupBy("fonte").agg(
    F.count("*").alias("qtd_linhas"),
    F.round(F.avg("fator_impacto"), 2).alias("impacto_medio"),
    F.round(F.max("fator_impacto"), 2).alias("impacto_maximo"),
).show()

df_join = (
    df_jcr.alias("j")
    .join(df_scimago.alias("s"), on="issn", how="inner")
    .select(
        F.col("issn"),
        F.col("j.titulo").alias("titulo"),
        F.col("j.total_citacoes").alias("citacoes_jcr"),
        F.col("s.total_citacoes").alias("citacoes_scimago"),
        F.col("j.fator_impacto").alias("impacto_jcr"),
        F.col("s.fator_impacto").alias("impacto_scimago"),
    )
)
print(f"Periodicos presentes nas duas fontes (join por ISSN): {df_join.count()}")

df_join.show(3, truncate=False)

print("\nTop 5 periodicos por fator de impacto (JCR):")
(
    df_jcr.orderBy(F.col("fator_impacto").desc())
    .select("titulo", "fator_impacto", "total_citacoes")
    .dropDuplicates(["titulo"])
    .orderBy(F.col("fator_impacto").desc())
    .show(5, truncate=False)
)

print("\nEstatisticas por fonte:")
df_uniao.groupBy("fonte").agg(
    F.count("*").alias("qtd_linhas"),
    F.round(F.avg("fator_impacto"), 2).alias("impacto_medio"),
    F.round(F.max("fator_impacto"), 2).alias("impacto_maximo"),
).show()

df_join.createOrReplaceTempView("periodicos")
print("\nTop 5 periodicos com maior discrepancia de citacoes entre fontes:")
spark.sql("""
    SELECT titulo,
           citacoes_jcr,
           citacoes_scimago,
           ABS(citacoes_jcr - citacoes_scimago) AS diferenca
    FROM periodicos
    ORDER BY diferenca DESC
    LIMIT 5
""").show(truncate=False)

df_join.write.mode("overwrite").parquet(SAIDA_PARQUET)
df_join.write.mode("overwrite").option("header", True).csv(SAIDA_CSV)

print(f"\nResultado gravado em:")
print(f"  {SAIDA_PARQUET}")
print(f"  {SAIDA_CSV}")
print(f"Conferencia - linhas no Parquet gravado: {spark.read.parquet(SAIDA_PARQUET).count()}")

spark.stop()