CREATE DATABASE auto_market_analysis;
USE auto_market_analysis;

SET SQL_SAFE_UPDATES = 0;

ALTER TABLE sales_by_brand
ADD COLUMN Month_Display VARCHAR(7);

UPDATE sales_by_brand
SET Month_Display = DATE_FORMAT(Month, '%Y-%m');

ALTER TABLE sales_by_segment
ADD COLUMN Month_Display VARCHAR(7);

UPDATE sales_by_segment
SET Month_Display = DATE_FORMAT(Month, '%Y-%m');

SET SQL_SAFE_UPDATES = 1;

# Per month market share by brand
WITH monthly_sales AS (
SELECT Month_Display, SUM(Units_sold) AS total_market_units
FROM sales_by_brand
GROUP BY Month_Display)

 SELECT s.Brand, s.Month_Display, s.Units_sold, ROUND(((100.0* s.Units_sold)/m.total_market_units), 2) AS market_share_pct
 FROM sales_by_brand s
 JOIN monthly_sales m ON s.Month_Display = m.Month_Display
 ORDER BY Month, market_share_pct DESC;
 
 # Calculating MoM growth rate for each brand
 SELECT Brand, Month_Display, Units_sold,
 LAG(Units_sold) OVER(PARTITION BY Brand ORDER BY Month_Display) AS prev_months_sale,
 ROUND((100.0*(Units_Sold - LAG(Units_sold) OVER(PARTITION BY Brand ORDER BY Month_Display)))
 /NULLIF((LAG(Units_sold) OVER(PARTITION BY Brand ORDER BY Month_Display)),0), 1) AS mom_growth_pct
 FROM sales_by_brand
ORDER BY Brand, Month;

# Ranking brands by annual sales

WITH annual_sales AS (
SELECT Brand, SUM(Units_sold) AS total_units
FROM sales_by_brand
GROUP BY Brand)

 SELECT *, RANK() OVER(ORDER BY total_units DESC) AS brand_rank
 FROM annual_Sales
 ORDER BY brand_rank;
 
 # Finding out the fastest-growing brands by comparing q1 vs q4 sales
WITH q1 AS (
SELECT Brand,  SUM(Units_sold) AS q1_units
FROM sales_by_brand
WHERE MONTH(Month) BETWEEN 1 AND 3
GROUP BY Brand),
q4 AS (
SELECT Brand,  SUM(Units_sold) AS q4_units
FROM sales_by_brand
WHERE MONTH(Month) BETWEEN 10 AND 12
GROUP BY Brand)

SELECT q1.Brand, q1.q1_units, q4.q4_units,
ROUND(((100.0*(q4.q4_units - q1.q1_units))/NULLIF(q1.q1_units, 0)), 2) AS full_year_growth
FROM q1 JOIN q4 ON q1.Brand = q4.Brand
ORDER BY full_year_growth DESC;

# Getting the top model of each brand according to total sales
WITH model_totals AS (
    SELECT Brand, Model, SUM(Units_sold) AS total_sales
    FROM brand_model
    GROUP BY Brand, Model
),
ranked_models AS (
    SELECT Brand, Model, total_sales,
	RANK() OVER (PARTITION BY Brand ORDER BY total_sales DESC) AS model_rank
    FROM model_totals)
SELECT Brand, Model, total_sales
FROM ranked_models
WHERE model_rank = 1
ORDER BY Brand;