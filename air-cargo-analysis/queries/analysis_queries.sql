-- ============================================================
-- AIR CARGO OPERATIONS ANALYSIS
-- Author: Alekhya Ghosh
-- Description: SQL analysis of air cargo operations covering
--              route performance, revenue, and service quality
-- ============================================================


-- ============================================================
-- 1. ROUTE PERFORMANCE: Top routes by total revenue
-- ============================================================
SELECT
    a1.city AS origin_city,
    a2.city AS destination_city,
    f.origin || ' → ' || f.destination AS route,
    COUNT(DISTINCT f.flight_id) AS total_flights,
    ROUND(SUM(cs.revenue_usd), 2) AS total_revenue_usd,
    ROUND(AVG(cs.revenue_usd), 2) AS avg_revenue_per_shipment,
    ROUND(SUM(cs.weight_kg), 1) AS total_cargo_kg
FROM flights f
JOIN cargo_shipments cs ON f.flight_id = cs.flight_id
JOIN airports a1 ON f.origin = a1.airport_code
JOIN airports a2 ON f.destination = a2.airport_code
GROUP BY f.origin, f.destination
ORDER BY total_revenue_usd DESC
LIMIT 10;


-- ============================================================
-- 2. CARGO TYPE ANALYSIS: Revenue and volume by cargo type
-- ============================================================
SELECT
    cargo_type,
    COUNT(*) AS total_shipments,
    ROUND(SUM(weight_kg), 1) AS total_weight_kg,
    ROUND(SUM(revenue_usd), 2) AS total_revenue_usd,
    ROUND(AVG(revenue_usd / weight_kg), 2) AS avg_rate_per_kg,
    ROUND(100.0 * SUM(revenue_usd) / (SELECT SUM(revenue_usd) FROM cargo_shipments), 2) AS revenue_share_pct
FROM cargo_shipments
GROUP BY cargo_type
ORDER BY total_revenue_usd DESC;


-- ============================================================
-- 3. AIRLINE PERFORMANCE: On-time rate and revenue by airline
-- ============================================================
SELECT
    al.airline_name,
    al.airline_type,
    COUNT(DISTINCT f.flight_id) AS total_flights,
    ROUND(100.0 * SUM(CASE WHEN f.actual_departure <= f.scheduled_departure THEN 1 ELSE 0 END)
          / COUNT(f.flight_id), 1) AS on_time_rate_pct,
    ROUND(SUM(cs.revenue_usd), 2) AS total_revenue_usd,
    ROUND(AVG(cs.revenue_usd), 2) AS avg_revenue_per_shipment
FROM flights f
JOIN airlines al ON f.airline_code = al.airline_code
JOIN cargo_shipments cs ON f.flight_id = cs.flight_id
GROUP BY al.airline_name, al.airline_type
ORDER BY total_revenue_usd DESC;


-- ============================================================
-- 4. MONTHLY REVENUE TREND: Revenue over time
-- ============================================================
SELECT
    STRFTIME('%Y-%m', departure_date) AS month,
    COUNT(DISTINCT f.flight_id) AS flights_operated,
    COUNT(cs.shipment_id) AS total_shipments,
    ROUND(SUM(cs.revenue_usd), 2) AS monthly_revenue_usd,
    ROUND(AVG(cs.weight_kg), 1) AS avg_shipment_weight_kg
FROM flights f
JOIN cargo_shipments cs ON f.flight_id = cs.flight_id
GROUP BY month
ORDER BY month;


-- ============================================================
-- 5. LOAD FACTOR ANALYSIS: Capacity utilisation by route
-- ============================================================
SELECT
    f.origin || ' → ' || f.destination AS route,
    COUNT(DISTINCT f.flight_id) AS flights,
    ROUND(AVG(f.capacity_kg), 0) AS avg_capacity_kg,
    ROUND(AVG(route_weight.total_weight), 1) AS avg_loaded_kg,
    ROUND(100.0 * AVG(route_weight.total_weight) / AVG(f.capacity_kg), 1) AS avg_load_factor_pct
FROM flights f
JOIN (
    SELECT flight_id, SUM(weight_kg) AS total_weight
    FROM cargo_shipments
    GROUP BY flight_id
) route_weight ON f.flight_id = route_weight.flight_id
GROUP BY f.origin, f.destination
HAVING flights >= 5
ORDER BY avg_load_factor_pct DESC
LIMIT 10;


-- ============================================================
-- 6. COMPLAINT ANALYSIS: Volume and resolution by type
-- ============================================================
SELECT
    c.complaint_type,
    COUNT(*) AS total_complaints,
    SUM(c.resolved) AS resolved_count,
    ROUND(100.0 * SUM(c.resolved) / COUNT(*), 1) AS resolution_rate_pct,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM complaints), 1) AS share_of_total_pct
FROM complaints c
GROUP BY c.complaint_type
ORDER BY total_complaints DESC;


-- ============================================================
-- 7. OPERATIONAL BOTTLENECKS: Routes with highest complaint rate
-- ============================================================
SELECT
    f.origin || ' → ' || f.destination AS route,
    COUNT(DISTINCT f.flight_id) AS total_flights,
    COUNT(c.complaint_id) AS total_complaints,
    ROUND(100.0 * COUNT(c.complaint_id) / COUNT(DISTINCT f.flight_id), 1) AS complaints_per_100_flights,
    ROUND(SUM(cs.revenue_usd), 2) AS total_revenue_usd
FROM flights f
LEFT JOIN complaints c ON f.flight_id = c.flight_id
LEFT JOIN cargo_shipments cs ON f.flight_id = cs.flight_id
GROUP BY f.origin, f.destination
HAVING total_flights >= 5
ORDER BY complaints_per_100_flights DESC
LIMIT 10;


-- ============================================================
-- 8. HIGH VALUE SHIPMENTS: Top shipments by revenue
-- ============================================================
SELECT
    cs.shipment_id,
    f.flight_number,
    f.origin || ' → ' || f.destination AS route,
    cs.cargo_type,
    ROUND(cs.weight_kg, 1) AS weight_kg,
    ROUND(cs.revenue_usd, 2) AS revenue_usd,
    ROUND(cs.revenue_usd / cs.weight_kg, 2) AS rate_per_kg,
    f.departure_date
FROM cargo_shipments cs
JOIN flights f ON cs.flight_id = f.flight_id
ORDER BY cs.revenue_usd DESC
LIMIT 15;
