

-- grafico comparacao por produto
select
	vp.descricao,
	max(vp.valor_unid) as "valor unitatio",
	sum(vv.quantidade) as "volume",
	(max(vp.valor_unid) * sum(vv.quantidade)) as "faturamento"
from vendas_produto vp
	inner join vendas_venda vv on vv.produto_id = vp.id
--where extract (month  from vv.data_lancamento ) = 2
group by vp.descricao
order by vp.descricao



select
	t.mes, t.descricao,
	(
		select vp2.valor_unid
		from vendas_produto vp2
		where
			vp2.id = t.id_produto
			-- TODO REALIZAR WHERE DE ANO E MES
	) as "valor_unid"
	(
		select vv2.quantidade
		from vendas_venda vv2
		where
			vv2.id = t.id
			and EXTRACT(YEAR FROM vv2.data_lancamento) = EXTRACT(YEAR FROM t.data_lancamento)
			and EXTRACT(MONTH FROM vv2.data_lancamento) = EXTRACT(MONTH FROM t.data_lancamento)
	) as "quantidade"
	TODO (MAX(t.valor_unid) * sum(t.quantidade)) as "faturamento"
from (
	select
		vv.id,
		EXTRACT(YEAR FROM vv.data_lancamento) as "ano",
		EXTRACT(MONTH FROM vv.data_lancamento) as "mes",
		vp.id as "id_produto",
		vp.descricao,
		vp.valor_unid,
		vv.quantidade
	from vendas_venda vv
		inner join vendas_produto vp on vv.produto_id = vp.id
		-- TODO REALIZAR WHERE ANO E PRODUTO
--	where
--		EXTRACT(YEAR FROM vv.data_lancamento) = 2019
--		and vp.id  = 1
) t
group by t.mes, t.descricao
order by t.mes, t.descricao




INSERT INTO public.vendas_venda (quantidade, data_lancamento, mesa_id, produto_id)
VALUES
    (1, '2020-02-1 00:00:00.000', 1, 3),
    (2, '2020-02-1 00:00:00.000', 2, 2),
    (3, '2020-02-1 00:00:00.000', 3, 1),
    (4, '2020-02-1 00:00:00.000', 4, 2),
    (5, '2020-02-1 00:00:00.000', 5, 3),
    (6, '2020-02-1 00:00:00.000', 6, 1),
    (7, '2020-02-1 00:00:00.000', 7, 2),
    (8, '2020-02-1 00:00:00.000', 8, 2),
    (9, '2020-02-1 00:00:00.000', 9, 3),
    (1, '2020-03-1 00:00:00.000', 1, 3),
    (2, '2020-03-1 00:00:00.000', 2, 2),
    (3, '2020-03-1 00:00:00.000', 3, 1),
    (4, '2020-03-1 00:00:00.000', 4, 2),
    (5, '2020-03-1 00:00:00.000', 5, 3),
    (6, '2020-03-1 00:00:00.000', 6, 1),
    (7, '2020-03-1 00:00:00.000', 7, 2),
    (8, '2020-03-1 00:00:00.000', 8, 2),
    (9, '2020-03-1 00:00:00.000', 9, 3),
    (1, '2020-04-1 00:00:00.000', 1, 3),
    (2, '2020-04-1 00:00:00.000', 2, 2),
    (3, '2020-04-1 00:00:00.000', 3, 1),
    (4, '2020-04-1 00:00:00.000', 4, 2),
    (5, '2020-04-1 00:00:00.000', 5, 3),
    (6, '2020-04-1 00:00:00.000', 6, 1),
    (7, '2020-04-1 00:00:00.000', 7, 2),
    (8, '2020-04-1 00:00:00.000', 8, 2),
    (9, '2020-04-1 00:00:00.000', 9, 3),
    (1, '2020-05-1 00:00:00.000', 1, 3),
    (2, '2020-05-1 00:00:00.000', 2, 2),
    (3, '2020-05-1 00:00:00.000', 3, 1),
    (4, '2020-05-1 00:00:00.000', 4, 2),
    (5, '2020-05-1 00:00:00.000', 5, 3),
    (6, '2020-05-1 00:00:00.000', 6, 1),
    (7, '2020-05-1 00:00:00.000', 7, 2),
    (8, '2020-05-1 00:00:00.000', 8, 2),
    (9, '2020-05-1 00:00:00.000', 9, 3),
    (1, '2020-06-1 00:00:00.000', 1, 3),
    (2, '2020-06-1 00:00:00.000', 2, 2),
    (3, '2020-06-1 00:00:00.000', 3, 1),
    (4, '2020-06-1 00:00:00.000', 4, 2),
    (5, '2020-06-1 00:00:00.000', 5, 3),
    (6, '2020-06-1 00:00:00.000', 6, 1),
    (7, '2020-06-1 00:00:00.000', 7, 2),
    (8, '2020-06-1 00:00:00.000', 8, 2),
    (9, '2020-06-1 00:00:00.000', 9, 3),
    (1, '2020-07-1 00:00:00.000', 1, 3),
    (2, '2020-07-1 00:00:00.000', 2, 2),
    (3, '2020-07-1 00:00:00.000', 3, 1),
    (4, '2020-07-1 00:00:00.000', 4, 2),
    (5, '2020-07-1 00:00:00.000', 5, 3),
    (6, '2020-07-1 00:00:00.000', 6, 1),
    (7, '2020-07-1 00:00:00.000', 7, 2),
    (8, '2020-07-1 00:00:00.000', 8, 2),
    (9, '2020-07-1 00:00:00.000', 9, 3);