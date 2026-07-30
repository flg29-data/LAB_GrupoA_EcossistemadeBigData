from __future__ import annotations

import os
import sys

import dlt
from dlt.sources.sql_database import sql_table
from sqlalchemy.engine import URL


def required_environment(name: str) -> str:
    value = os.environ.get(name)

    if not value:
        raise RuntimeError(
            f"Variável obrigatória ausente: {name}"
        )

    return value


def main() -> int:
    password = required_environment("DLT_DB_PASSWORD")

    connection_url = URL.create(
        drivername="postgresql+psycopg2",
        username=required_environment("DLT_DB_USER"),
        password=password,
        host=required_environment("DLT_DB_HOST"),
        port=int(required_environment("DLT_DB_PORT")),
        database=required_environment("DLT_DB_NAME"),
    ).render_as_string(hide_password=False)

    pipeline = dlt.pipeline(
        pipeline_name="ingestao_postgres_dlt",
        destination="filesystem",
        dataset_name="postgres",
    )

    vendas = sql_table(
        credentials=connection_url,
        schema="public",
        table="vendas",
    )

    print("=" * 70)
    print("PIPELINE POSTGRESQL → S3 — DLT")
    print("=" * 70)
    print("Origem=RDS PostgreSQL")
    print("Schema=public")
    print("Tabela=vendas")
    print("Destino=filesystem/S3")
    print("Dataset=postgres")
    print("Formato=parquet")
    print("SenhaExibida=NAO")
    print()

    try:
        load_info = pipeline.run(
            vendas,
            loader_file_format="parquet",
            write_disposition="replace",
        )
    except Exception as exc:
        safe_message = str(exc).replace(
            password,
            "<SEGREDO_REMOVIDO>",
        )

        print(f"ErroTipo={type(exc).__name__}")
        print(f"ErroMensagem={safe_message}")
        print("Resultado=REVISAR")
        return 1

    print(load_info)
    print()
    print(f"PipelineName={pipeline.pipeline_name}")
    print(f"DatasetName={pipeline.dataset_name}")
    print("Resultado=EXECUCAO_CONCLUIDA")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
