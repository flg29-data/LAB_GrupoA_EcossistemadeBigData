from __future__ import annotations

import sys

import dlt
from dlt.sources.rest_api import rest_api_source


def main() -> int:
    source = rest_api_source(
        {
            "client": {
                "base_url": (
                    "https://pokeapi.co/api/v2/"
                ),
            },
            "resources": [
                {
                    "name": "pokemon",
                    "write_disposition": "replace",
                    "endpoint": {
                        "path": "pokemon",
                        "data_selector": "results",
                        "paginator": {
                            "type": "offset",
                            "limit": 100,
                            "offset": 0,
                            "limit_param": "limit",
                            "offset_param": "offset",
                            "total_path": "count",
                        },
                    },
                }
            ],
        }
    )

    pipeline = dlt.pipeline(
        pipeline_name="ingestao_pokeapi_dlt",
        destination="filesystem",
        dataset_name="pokeapi",
    )

    print("=" * 70)
    print("PIPELINE POKÉAPI → S3 — DLT")
    print("=" * 70)
    print("Origem=https://pokeapi.co/api/v2/pokemon")
    print("Recurso=pokemon")
    print("Paginacao=offset")
    print("OffsetInicial=0")
    print("LimitePorPagina=100")
    print("TotalPath=count")
    print("MaximumOffset=NAO_APLICADO")
    print("Destino=filesystem/S3")
    print("Dataset=pokeapi")
    print("Formato=parquet")
    print("CredencialAPI=NAO_NECESSARIA")
    print()

    try:
        load_info = pipeline.run(
            source,
            loader_file_format="parquet",
        )
    except Exception as exc:
        print(f"ErroTipo={type(exc).__name__}")
        print(f"ErroMensagem={exc}")
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
