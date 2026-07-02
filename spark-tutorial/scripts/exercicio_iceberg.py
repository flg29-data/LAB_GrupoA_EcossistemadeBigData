from pathlib import Path
from pyspark.sql import SparkSession, functions as F

BASE_DIR = Path(__file__).resolve().parent.parent
ARQUIVO_JCR = str(BASE_DIR / "data" / "jcr.csv")
ARQUIVO_SCIMAGO = str(BASE_DIR / "data" / "scimago.csv")
WAREHOUSE = str(BASE_DIR / "warehouse")

spark = (
    SparkSession.builder
    .appName("ExercicioIceberg")
    .master("local[*]")
    .config("spark.driver.bindAddress", "127.0.0.1")
    .config("spark.driver.host", "127.0.0.1")
    .config("spark.jars.packages",
            "org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.10.2")
    .config("spark.sql.extensions",
            "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions")
    .config("spark.sql.catalog.local", "org.apache.iceberg.spark.SparkCatalog")
    .config("spark.sql.catalog.local.type", "hadoop")
    .config("spark.sql.catalog.local.warehouse", WAREHOUSE)
    .getOrCreate()
)
spark.sparkContext.setLogLevel("ERROR")
print(f"Spark {spark.version} + Iceberg prontos. Warehouse: {WAREHOUSE}")

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
        .dropna(subset=["fator_impacto"])
    )

df_jcr = padronizar(spark.read.csv(ARQUIVO_JCR, header=True, inferSchema=True))
df_scimago = padronizar(spark.read.csv(ARQUIVO_SCIMAGO, header=True, inferSchema=True))

df_periodicos = (
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
print(f"Linhas a gravar na tabela Iceberg: {df_periodicos.count()}")

df_periodicos.writeTo("local.db.periodicos").createOrReplace()
spark.sql("SELECT COUNT(*) AS qtd FROM local.db.periodicos").show()
print("Tabela local.db.periodicos criada com sucesso")

print("\nAntes do UPDATE:")
spark.sql("""
    SELECT titulo, impacto_jcr FROM local.db.periodicos
    WHERE titulo = 'CA-A CANCER JOURNAL FOR CLINICIANS'
""").show(truncate=False)

spark.sql("""
    UPDATE local.db.periodicos
    SET impacto_jcr = 999.9
    WHERE titulo = 'CA-A CANCER JOURNAL FOR CLINICIANS'
""")

print("Depois do UPDATE:")
spark.sql("""
    SELECT titulo, impacto_jcr FROM local.db.periodicos
    WHERE titulo = 'CA-A CANCER JOURNAL FOR CLINICIANS'
""").show(truncate=False)

print("Historico de snapshots da tabela:")
spark.sql("""
    SELECT snapshot_id, committed_at, operation
    FROM local.db.periodicos.snapshots
    ORDER BY committed_at
""").show(truncate=False)

snap_criacao = spark.sql("""
    SELECT snapshot_id FROM local.db.periodicos.snapshots
    ORDER BY committed_at LIMIT 1
""").first()["snapshot_id"]

print(f"TIME TRAVEL para o snapshot de criacao ({snap_criacao}):")
spark.sql(f"""
    SELECT titulo, impacto_jcr
    FROM local.db.periodicos VERSION AS OF {snap_criacao}
    WHERE titulo = 'CA-A CANCER JOURNAL FOR CLINICIANS'
""").show(truncate=False)

print("Consulta atual (sem time travel):")
spark.sql("""
    SELECT titulo, impacto_jcr FROM local.db.periodicos
    WHERE titulo = 'CA-A CANCER JOURNAL FOR CLINICIANS'
""").show(truncate=False)

spark.stop()