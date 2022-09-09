AVERAGE_PRICES = """
WITH RECURSIVE origin_regions AS (
    SELECT *
    FROM regions
    WHERE slug = :origin
  UNION ALL
    SELECT r.*
    FROM regions r
        INNER JOIN origin_regions o ON r.parent_slug = o.slug
), destination_regions AS (
    SELECT *
    FROM regions
    WHERE slug = :destination
  UNION ALL
    SELECT r.*
    FROM regions r
    INNER JOIN destination_regions d ON r.parent_slug = d.slug
), origins AS (
    SELECT p.code, p.name, r.slug AS region, r.name AS region_name
    FROM ports p LEFT JOIN regions r ON p.parent_slug = r.slug
    WHERE p.code = :origin
  UNION ALL
    SELECT p.code, p.name, o.slug AS region, o.name AS region_name
    FROM ports p
        INNER JOIN origin_regions o ON p.parent_slug = o.slug
), destinations AS (
    SELECT p.code, p.name, r.slug AS region, r.name AS region_name
    FROM ports p LEFT JOIN regions r ON p.parent_slug = r.slug
    WHERE p.code = :destination
  UNION ALL
    SELECT p.code, p.name, d.slug AS region, d.name AS region_name
    FROM ports p
        INNER JOIN destination_regions d ON p.parent_slug = d.slug
), dates AS (
    SELECT date_trunc('day', dt)::date AS day
    FROM generate_series(:date_from, :date_to, '1 day'::interval) dt
), avgprices AS (
    SELECT s.day,
           AVG(s.price) AS average_price,
           COUNT(*) AS prices_in_day
    FROM prices s
        INNER JOIN origins o ON s.orig_code = o.code
        INNER JOIN destinations d ON s.dest_code = d.code
    WHERE s.day >= :date_from AND s.day <= :date_to
    GROUP BY s.day
)
SELECT d.day,
       CASE
           WHEN prices_in_day < 3 THEN NULL
           ELSE ROUND(p.average_price, 2)
       END AS average_price
FROM dates d
    LEFT JOIN avgprices p ON d.day = p.day
"""
