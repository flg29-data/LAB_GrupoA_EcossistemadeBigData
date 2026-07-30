BEGIN;

DROP TABLE IF EXISTS vendas;
DROP TABLE IF EXISTS produtos;
DROP TABLE IF EXISTS clientes;

CREATE TABLE clientes (
    cliente_id  SERIAL PRIMARY KEY,
    nome        VARCHAR(120) NOT NULL,
    email       VARCHAR(160) NOT NULL UNIQUE,
    cidade      VARCHAR(100) NOT NULL,
    estado      CHAR(2) NOT NULL,
    criado_em   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE produtos (
    produto_id  SERIAL PRIMARY KEY,
    nome        VARCHAR(150) NOT NULL,
    categoria   VARCHAR(100) NOT NULL,
    preco       NUMERIC(12,2) NOT NULL CHECK (preco >= 0),
    estoque     INTEGER NOT NULL CHECK (estoque >= 0),
    criado_em   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE vendas (
    venda_id       BIGSERIAL PRIMARY KEY,
    cliente_id     INTEGER NOT NULL REFERENCES clientes(cliente_id),
    produto_id     INTEGER NOT NULL REFERENCES produtos(produto_id),
    data_venda     TIMESTAMP NOT NULL,
    quantidade     INTEGER NOT NULL CHECK (quantidade > 0),
    valor_unitario NUMERIC(12,2) NOT NULL CHECK (valor_unitario >= 0),
    desconto       NUMERIC(5,4) NOT NULL DEFAULT 0
                   CHECK (desconto >= 0 AND desconto <= 1)
);

CREATE INDEX idx_vendas_cliente
    ON vendas (cliente_id);

CREATE INDEX idx_vendas_produto
    ON vendas (produto_id);

CREATE INDEX idx_vendas_data
    ON vendas (data_venda);

COMMIT;