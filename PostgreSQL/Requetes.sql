/*Total des ventes mensuelles par magasin"*/
SELECT 
    s.shop_name, 
    st.year, 
    st.month, 
    SUM(st.vente_mensuel) AS total_ventes
FROM sales_train st
JOIN shops s ON st.shop_id = s.shop_id
GROUP BY s.shop_name, st.year, st.month
ORDER BY st.year, st.month, total_ventes DESC
LIMIT 10;

/*Ventes totales par produit et par catégorie"*/
SELECT 
    ic.item_category_name, 
    i.item_name, 
    SUM(st.item_cnt_day) AS total_produits_vendus
FROM sales_train st
JOIN items i ON st.item_id = i.item_id
JOIN item_categories ic ON i.item_category_id = ic.item_category_id
GROUP BY ic.item_category_name, i.item_name
ORDER BY total_produits_vendus DESC
LIMIT 10;

/*Prix moyen des produits vendus par magasin*/
SELECT 
    s.shop_name, 
    AVG(st.item_price) AS prix_moyen
FROM sales_train st
JOIN shops s ON st.shop_id = s.shop_id
GROUP BY s.shop_name
ORDER BY prix_moyen DESC
LIMIT 10;

/*Magasins avec les meilleures ventes pour un produit spécifique*/
SELECT 
    s.shop_name, 
    SUM(st.item_cnt_day) AS total_produits_vendus
FROM sales_train st
JOIN shops s ON st.shop_id = s.shop_id
WHERE st.item_id = 100  
GROUP BY s.shop_name
ORDER BY total_produits_vendus DESC
LIMIT 10;

/*Nombre de ventes par catégorie et par mois*/
SELECT 
    ic.item_category_name, 
    st.year, 
    st.month, 
    SUM(st.item_cnt_day) AS ventes_mensuelles
FROM sales_train st
JOIN items i ON st.item_id = i.item_id
JOIN item_categories ic ON i.item_category_id = ic.item_category_id
GROUP BY ic.item_category_name, st.year, st.month
ORDER BY st.year, st.month, ventes_mensuelles DESC;

/* Magasins avec les ventes les plus élevées pour une catégorie spécifique */
SELECT 
	sh.shop_name,
	ic.item_category_name,
	SUM(st.item_cnt_day) AS total_ventes

FROM sales_train st
JOIN shops sh ON st.shop_id=sh.shop_id
JOIN items it ON st.item_id=it.item_id
JOIN item_categories ic ON it.item_category_id=ic.item_category_id
WHERE ic.item_category_id=2
GROUP BY sh.shop_name, ic.item_category_name
ORDER BY total_ventes DESC
LIMIT 10;

/*Ventes moyennes par jour de la semaine*/
SELECT 
    EXTRACT(DOW FROM st.date) AS jour_semaine,  -- DOW = Day Of Week
    AVG(st.item_cnt_day) AS ventes_moyennes
FROM 
    sales_train st
GROUP BY 
    jour_semaine
ORDER BY 
    jour_semaine;

/*Produits avec les meilleures ventes sur une période donnée*/
SELECT
	it.item_name,
	SUM(st.item_cnt_day) AS total_produits_vendus
FROM sales_train st
JOIN items it ON st.item_id=it.item_id
WHERE st.date BETWEEN '2013-01-02' AND '2013-01-15'
GROUP BY 
    it.item_name
ORDER BY 
    total_produits_vendus DESC
LIMIT 10;

/* Ventes mensuelles par produit et magasin */
SELECT 
    sh.shop_name, 
    it.item_name, 
    st.year, 
    st.month, 
    SUM(st.item_cnt_day) AS total_produits_vendus
FROM sales_train st
JOIN shops sh ON st.shop_id = sh.shop_id
JOIN items it ON st.item_id = it.item_id
GROUP BY sh.shop_name, it.item_name, st.year, st.month
ORDER BY st.year, st.month, total_produits_vendus DESC
LIMIT;
