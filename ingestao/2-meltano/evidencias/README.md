# Evidências — Tutorial 2 AWS: Meltano

Pasta destinada ao registro das evidências de execução do Tutorial 2, realizado em uma instância EC2 com extração de dados do RDS PostgreSQL e da PokéAPI, geração de arquivos Parquet e preparação para publicação no Amazon S3.

## Resultado comprovado pelos registros disponíveis

| Etapa | Situação | Evidência |
|---|---|---|
| Conexão EC2 → RDS PostgreSQL | Concluída | `logs/01-validacao-rds.log` |
| Configuração SSL do `tap-postgres` | Concluída | `logs/02-configuracao-tap-postgres.log` |
| Extração da tabela `vendas` | Concluída | `logs/03-ingestao-postgres.log` |
| Geração do Parquet de vendas | Concluída | `logs/05-validacao-arquivos-parquet.log` |
| Extração da PokéAPI | Concluída | `logs/04-ingestao-pokeapi.log` |
| Geração do Parquet da PokéAPI | Concluída | `logs/05-validacao-arquivos-parquet.log` |
| Publicação no S3 | Pendente de comprovação final | `logs/06-diagnostico-upload-s3.log` |

## Resultados observados

- 200 registros encontrados na tabela `vendas` do banco `ecommerce`.
- Pipeline PostgreSQL finalizada com código de saída `0`.
- Arquivo `public-vendas-20260719_025026-0-0.gz.parquet`, com 5.605 bytes.
- 1.350 registros processados pela pipeline da PokéAPI.
- Pipeline PokéAPI finalizada com código de saída `0`.
- Arquivo `pokemon-20260719_025128-0-0.gz.parquet`, com 16.177 bytes.
- O primeiro upload ao S3 falhou porque a variável `BUCKET` continha um caractere invisível `\r`, resultando em 26 caracteres em vez de 25.

## Pendência documental

Os registros fornecidos não contêm uma saída bem-sucedida do `aws s3 sync` após a correção do caractere `\r`. Por esse motivo, esta pasta não declara como comprovada a publicação final dos Parquet no S3.

Execute `scripts/08-finalizar-upload-s3.sh` dentro da EC2 e copie os novos logs para esta pasta. O script gera evidências da correção, do upload e da listagem final do S3.

## Segurança

Nenhum arquivo desta pasta contém:

- senha do RDS;
- arquivo `.env`;
- credenciais da AWS;
- chave `labsuser.pem`;
- arquivos de estado do Terraform.
