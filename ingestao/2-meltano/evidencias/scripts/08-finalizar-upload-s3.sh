#!/usr/bin/env bash
set -euo pipefail

# Executar dentro da EC2, no diretório do projeto Meltano.
# O script não contém credenciais e usa o papel IAM da instância.

EVIDENCIAS="${HOME}/evidencias_tutorial2"
mkdir -p "$EVIDENCIAS"

if [[ -f "${HOME}/tutorial2_env.sh" ]]; then
  sed -i 's/\r$//' "${HOME}/tutorial2_env.sh"
  # shellcheck disable=SC1090
  source "${HOME}/tutorial2_env.sh"
fi

BUCKET="$(printf '%s' "${BUCKET:-}" | tr -d '\r\n')"
export BUCKET

if [[ -z "$BUCKET" ]]; then
  echo "ERRO: a variável BUCKET não foi definida." >&2
  exit 1
fi

{
  printf 'BUCKET técnico: <%q>\n' "$BUCKET"
  printf 'Quantidade de caracteres: %s\n' "${#BUCKET}"
  aws s3api head-bucket --bucket "$BUCKET" --region us-east-1
} 2>&1 | tee "$EVIDENCIAS/08-validacao-bucket-s3.log"

aws s3 sync \
  output/public-vendas \
  "s3://${BUCKET}/meltano/vendas/" \
  --exclude "*" \
  --include "*.parquet" \
  2>&1 | tee "$EVIDENCIAS/09-upload-vendas-s3.log"

aws s3 sync \
  output/pokemon \
  "s3://${BUCKET}/meltano/pokemon/" \
  --exclude "*" \
  --include "*.parquet" \
  2>&1 | tee "$EVIDENCIAS/10-upload-pokemon-s3.log"

aws s3 ls \
  "s3://${BUCKET}/meltano/" \
  --recursive \
  2>&1 | tee "$EVIDENCIAS/11-validacao-final-s3.log"

aws s3api list-objects-v2 \
  --bucket "$BUCKET" \
  --prefix "meltano/" \
  --query 'Contents[].{Arquivo:Key,Tamanho_bytes:Size}' \
  --output table \
  2>&1 | tee "$EVIDENCIAS/12-inventario-s3.log"

echo "Evidências finais gravadas em: $EVIDENCIAS"
