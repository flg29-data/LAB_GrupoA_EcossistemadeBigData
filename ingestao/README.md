# Tutoriais de Ingestão de Dados

Conjunto de tutoriais práticos sobre **ingestão de dados** para transportar dados de um banco relacional (**PostgreSQL**) e de uma API REST pública (**PokéAPI**) para um **data lake S3**, em formato **Parquet**.

Os laboratórios podem ser executados:

- **localmente**, com Docker e MiniStack;
- **na AWS**, com Amazon RDS, Amazon EC2 e Amazon S3, provisionados com Terraform.

Cada tutorial contém duas versões:

- **`TUTORIAL.md`** — versão longa, didática e explicativa;
- **`QUICK_TUTORIAL.md`** — versão resumida, concentrada nos comandos.

---

## Ordem recomendada

```text
1) Infraestrutura  ──►  2) Meltano
                  └──►  3) DLTHub + Python
```

O **Tutorial 1** prepara a infraestrutura, o banco de dados e o destino. Os Tutoriais **2** e **3** são independentes entre si e apresentam ferramentas diferentes para realizar a ingestão.

| # | Tutorial | Local | AWS |
|---|---|---|---|
| 1 | **Infraestrutura** | [`1-infraestrutura/local`](1-infraestrutura/local/TUTORIAL.md) — Docker, PostgreSQL e MiniStack | [`1-infraestrutura/aws`](1-infraestrutura/aws/TUTORIAL.md) — Terraform, RDS, EC2 e S3 |
| 2 | **Meltano** | [`2-meltano/local`](2-meltano/local/TUTORIAL.md) | [`2-meltano/aws`](2-meltano/aws/TUTORIAL.md) |
| 3 | **DLTHub + Python** | [`3-dlthub/local`](3-dlthub/local/TUTORIAL.md) | [`3-dlthub/aws`](3-dlthub/aws/TUTORIAL.md) |

---

## Arquitetura dos laboratórios AWS

```text
                         AWS — us-east-1

 ┌─────────────────┐       ┌────────────────────────┐
 │ RDS PostgreSQL  │──────►│                        │
 │ banco ecommerce │       │ EC2 runner            │
 │ tabela vendas   │       │ Meltano ou dlt/Python │──────► Amazon S3
 └─────────────────┘       │                        │        arquivos Parquet
                            └────────────────────────┘
                                      ▲
                                      │ HTTPS
                              ┌──────────────┐
                              │   PokéAPI    │
                              └──────────────┘
```

A instância EC2 utiliza o perfil IAM disponibilizado pelo AWS Academy Learner Lab. Dessa forma, o acesso ao S3 ocorre sem chaves AWS gravadas no código.

---

## Dados utilizados

Os dados de exemplo representam um comércio eletrônico e são compartilhados pelos três tutoriais.

| Tabela | Quantidade | Conteúdo |
|---|---:|---|
| `clientes` | 20 | cadastro de clientes |
| `produtos` | 15 | catálogo de produtos |
| `vendas` | 200 | tabela utilizada nas ingestões dos Tutoriais 2 e 3 |

Arquivos principais da pasta [`dados`](dados/):

- `schema.sql` — criação das tabelas;
- `seed.sql` — carga inicial do PostgreSQL;
- arquivos CSV de referência.

---

## Resultados da execução na AWS

### Tutorial 1 — Infraestrutura com Terraform

- provisionamento de uma instância EC2 runner;
- provisionamento de um RDS PostgreSQL privado;
- criação de um bucket S3 para o data lake;
- população do banco `ecommerce`;
- validação de 20 clientes, 15 produtos e 200 vendas;
- infraestrutura reutilizada pelos Tutoriais 2 e 3.

**Resultado técnico:** aprovado.  
**Resultado documental:** aprovado com ressalva, pois parte das evidências foi reconstruída a partir dos registros técnicos disponíveis.

Diretório: [`1-infraestrutura/aws`](1-infraestrutura/aws/)

Principais entregáveis previstos no diretório:

- `Relatorio_Final_Tutorial1_AWS_Terraform.docx`;
- `evidencias_tutorial1_aws.zip`;
- `E13_resumo_final_tutorial1.txt`.

### Tutorial 2 — Ingestão com Meltano

- Meltano 4.2.1 executado na EC2;
- extração de 200 registros da tabela `public.vendas` no RDS;
- extração de 1.351 registros únicos da PokéAPI;
- geração de arquivos Parquet;
- publicação no S3 nos prefixos `meltano/vendas/` e `meltano/pokemon/`;
- validação dos arquivos por contagem e hashes SHA-256.

**Resultado:** aprovado.

Diretório: [`2-meltano/aws`](2-meltano/aws/)

Principais entregáveis previstos no diretório:

- `Relatorio_Final_Tutorial2_AWS_Meltano.docx`;
- `evidencias_tutorial2_aws.zip`;
- `E55_resumo_final_tutorial2.txt`.

### Tutorial 3 — Ingestão com DLTHub e Python

- dlt 1.29.1 executado na EC2;
- extração de 200 registros da tabela `public.vendas` no RDS;
- extração de 1.351 registros únicos da PokéAPI;
- geração de arquivos Parquet;
- publicação no S3 nos prefixos `postgres/vendas/` e `pokeapi/pokemon/`;
- validação independente com `pyarrow` e `s3fs`;
- autenticação no S3 por perfil IAM, sem chaves estáticas no código.

**Resultado:** aprovado.

Diretório: [`3-dlthub/aws`](3-dlthub/aws/)

Principais entregáveis previstos no diretório:

- `Relatorio_Final_Tutorial3_AWS_DLTHub.docx`;
- `evidencias_tutorial3_dlthub_aws.zip`;
- `evidencias/09-validacao-final/E46_resumo_final_tutorial3.txt`.

---

## Estrutura principal

```text
ingestao/
├── 1-infraestrutura/
│   ├── local/
│   └── aws/
├── 2-meltano/
│   ├── local/
│   └── aws/
├── 3-dlthub/
│   ├── local/
│   └── aws/
├── dados/
└── README.md
```

Os diretórios AWS podem conter, além dos arquivos do tutorial:

- relatórios finais em DOCX;
- resumos consolidados em TXT;
- evidências de execução;
- inventários e hashes SHA-256;
- pacotes ZIP para entrega.

---

## Segurança

Não devem ser enviados ao GitHub:

- credenciais temporárias do AWS Academy;
- arquivos `credentials` e `config` da AWS;
- chaves privadas `*.pem`;
- pastas `.secrets/`;
- arquivos `.env` com senhas;
- `terraform.tfvars` com dados sensíveis;
- arquivos `*.tfstate` e planos `tfplan*`;
- ambientes virtuais Python e diretórios `.terraform/`.

Antes de cada commit, recomenda-se conferir os arquivos preparados:

```bash
git diff --cached --name-only
```

---

## Tecnologias utilizadas

- Terraform;
- AWS Academy Learner Lab;
- Amazon EC2;
- Amazon RDS for PostgreSQL;
- Amazon S3;
- PostgreSQL;
- Meltano;
- DLTHub (`dlt`);
- Python;
- Parquet;
- Git e GitHub.

---

## Observação sobre custos

EC2 e RDS podem gerar consumo enquanto estiverem ativos. A infraestrutura deve permanecer disponível durante a execução e a conferência dos três tutoriais. Após a conclusão definitiva, execute o procedimento de destruição indicado no Tutorial 1 AWS:

```bash
terraform destroy
```

Antes da destruição, confirme que os relatórios, evidências e arquivos necessários foram preservados fora dos recursos que serão removidos.
