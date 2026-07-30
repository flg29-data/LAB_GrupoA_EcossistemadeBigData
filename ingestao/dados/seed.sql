BEGIN;

TRUNCATE TABLE vendas, produtos, clientes
RESTART IDENTITY CASCADE;

INSERT INTO clientes (
    nome,
    email,
    cidade,
    estado,
    criado_em
)
SELECT
    'Cliente ' || LPAD(numero::TEXT, 2, '0'),
    'cliente' || LPAD(numero::TEXT, 2, '0') || '@exemplo.com',
    (ARRAY[
        'Rio de Janeiro',
        'Niteroi',
        'Sao Paulo',
        'Belo Horizonte',
        'Curitiba'
    ])[1 + ((numero - 1) % 5)],
    (ARRAY[
        'RJ',
        'RJ',
        'SP',
        'MG',
        'PR'
    ])[1 + ((numero - 1) % 5)],
    TIMESTAMP '2026-01-01 08:00:00'
        + ((numero - 1) * INTERVAL '1 day')
FROM generate_series(1, 20) AS numero;

INSERT INTO produtos (
    nome,
    categoria,
    preco,
    estoque,
    criado_em
)
SELECT
    'Produto ' || LPAD(numero::TEXT, 2, '0'),
    (ARRAY[
        'Eletronicos',
        'Informatica',
        'Escritorio',
        'Casa',
        'Livros'
    ])[1 + ((numero - 1) % 5)],
    ROUND((25 + numero * 17.35)::NUMERIC, 2),
    50 + numero * 10,
    TIMESTAMP '2026-01-01 09:00:00'
        + ((numero - 1) * INTERVAL '1 hour')
FROM generate_series(1, 15) AS numero;

INSERT INTO vendas (
    cliente_id,
    produto_id,
    data_venda,
    quantidade,
    valor_unitario,
    desconto
)
SELECT
    1 + ((serie.numero - 1) % 20),
    produto.produto_id,
    TIMESTAMP '2026-02-01 08:00:00'
        + ((serie.numero - 1) * INTERVAL '6 hours'),
    1 + ((serie.numero - 1) % 5),
    produto.preco,
    CASE
        WHEN serie.numero % 10 = 0 THEN 0.10
        WHEN serie.numero % 5 = 0 THEN 0.05
        ELSE 0.00
    END
FROM generate_series(1, 200) AS serie(numero)
JOIN produtos AS produto
  ON produto.produto_id = 1 + (((serie.numero * 7) - 1) % 15);

COMMIT;