-- =============================================
-- ANALISE 1: Receita total por mes
-- =============================================
SELECT
    DATE_TRUNC('month', o.order_purchase_timestamp::timestamp) AS mes,
    COUNT(DISTINCT o.order_id) AS total_pedidos,
    ROUND(SUM(p.payment_value)::numeric, 2) AS receita_total
FROM orders o
JOIN payments p ON o.order_id = p.order_id
WHERE o.order_status = 'delivered'
GROUP BY 1
ORDER BY 1;


-- =============================================
-- ANALISE 2: Top 10 categorias por receita
-- =============================================
SELECT
    t.product_category_name_english AS categoria,
    COUNT(DISTINCT oi.order_id) AS total_pedidos,
    ROUND(SUM(oi.price)::numeric, 2) AS receita_total,
    ROUND(AVG(oi.price)::numeric, 2) AS ticket_medio
FROM order_items oi
JOIN products pr ON oi.product_id = pr.product_id
JOIN category_translation t ON pr.product_category_name = t.product_category_name
GROUP BY 1
ORDER BY receita_total DESC
LIMIT 10;


-- =============================================
-- ANALISE 3: Taxa de entrega por estado
-- =============================================
SELECT
    c.customer_state AS estado,
    COUNT(*) AS total_pedidos,
    SUM(CASE WHEN o.order_status = 'delivered' THEN 1 ELSE 0 END) AS entregues,
    ROUND(
        100.0 * SUM(CASE WHEN o.order_status = 'delivered' THEN 1 ELSE 0 END) / COUNT(*),
        1
    ) AS taxa_entrega_pct
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
GROUP BY 1
HAVING COUNT(*) > 100
ORDER BY taxa_entrega_pct DESC;


-- =============================================
-- ANALISE 4: Tempo medio de entrega por estado
-- =============================================
SELECT
    c.customer_state AS estado,
    ROUND(AVG(
        EXTRACT(EPOCH FROM (
            o.order_delivered_customer_date::timestamp -
            o.order_purchase_timestamp::timestamp
        )) / 86400
    )::numeric, 1) AS dias_medio_entrega,
    COUNT(*) AS total_pedidos
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_delivered_customer_date IS NOT NULL
GROUP BY 1
HAVING COUNT(*) > 50
ORDER BY dias_medio_entrega ASC;


-- =============================================
-- ANALISE 5: Nota media dos vendedores (top 20)
-- =============================================
SELECT
    oi.seller_id,
    COUNT(DISTINCT oi.order_id) AS total_vendas,
    ROUND(AVG(r.review_score)::numeric, 2) AS nota_media,
    ROUND(SUM(oi.price)::numeric, 2) AS receita_total
FROM order_items oi
JOIN reviews r ON oi.order_id = r.order_id
GROUP BY 1
HAVING COUNT(DISTINCT oi.order_id) >= 50
ORDER BY nota_media DESC, total_vendas DESC
LIMIT 20;