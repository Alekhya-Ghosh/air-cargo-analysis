"""
Air Cargo Operations Analysis
Author: Alekhya Ghosh
Description: End-to-end SQL-driven analysis of air cargo operations.
             Covers route performance, revenue trends, load factors,
             cargo mix, and service quality metrics.
"""

import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

DB_PATH = r"C:\Users\ALEKHYA GHOSH\PycharmProjects\Air-Cargo-Analysis\air-cargo-analysis\data\air_cargo.db"
OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

conn = sqlite3.connect(DB_PATH)

print("=" * 60)
print("AIR CARGO OPERATIONS ANALYSIS")
print("=" * 60)

# ── 1. TOP ROUTES BY REVENUE ──────────────────────────────────
q1 = """
SELECT
    a1.city || ' → ' || a2.city AS route,
    COUNT(DISTINCT f.flight_id) AS total_flights,
    ROUND(SUM(cs.revenue_usd), 0) AS total_revenue_usd,
    ROUND(SUM(cs.weight_kg), 0) AS total_cargo_kg
FROM flights f
JOIN cargo_shipments cs ON f.flight_id = cs.flight_id
JOIN airports a1 ON f.origin = a1.airport_code
JOIN airports a2 ON f.destination = a2.airport_code
GROUP BY f.origin, f.destination
ORDER BY total_revenue_usd DESC
LIMIT 10
"""
df_routes = pd.read_sql(q1, conn)
print("\n[1] TOP 10 ROUTES BY REVENUE")
print(df_routes.to_string(index=False))

fig1 = px.bar(df_routes, x="total_revenue_usd", y="route", orientation="h",
              color="total_revenue_usd", color_continuous_scale="Oranges",
              title="Top 10 Routes by Total Revenue (USD)",
              labels={"total_revenue_usd": "Revenue (USD)", "route": "Route"})
fig1.update_layout(template="plotly_white", showlegend=False,
                   coloraxis_showscale=False, height=450)
fig1.write_html(f"{OUTPUT_DIR}/01_top_routes_revenue.html")

# ── 2. CARGO TYPE REVENUE SHARE ───────────────────────────────
q2 = """
SELECT
    cargo_type,
    COUNT(*) AS shipments,
    ROUND(SUM(revenue_usd), 0) AS total_revenue_usd,
    ROUND(AVG(revenue_usd / weight_kg), 2) AS avg_rate_per_kg
FROM cargo_shipments
GROUP BY cargo_type
ORDER BY total_revenue_usd DESC
"""
df_cargo = pd.read_sql(q2, conn)
print("\n[2] CARGO TYPE REVENUE BREAKDOWN")
print(df_cargo.to_string(index=False))

fig2 = px.pie(df_cargo, values="total_revenue_usd", names="cargo_type",
              title="Revenue Share by Cargo Type",
              color_discrete_sequence=px.colors.sequential.Oranges_r)
fig2.update_traces(textposition="inside", textinfo="percent+label")
fig2.update_layout(template="plotly_white", showlegend=True)
fig2.write_html(f"{OUTPUT_DIR}/02_cargo_type_revenue.html")

# ── 3. MONTHLY REVENUE TREND ──────────────────────────────────
q3 = """
SELECT
    STRFTIME('%Y-%m', f.departure_date) AS month,
    COUNT(DISTINCT f.flight_id) AS flights,
    ROUND(SUM(cs.revenue_usd), 0) AS monthly_revenue_usd,
    COUNT(cs.shipment_id) AS shipments
FROM flights f
JOIN cargo_shipments cs ON f.flight_id = cs.flight_id
GROUP BY month
ORDER BY month
"""
df_monthly = pd.read_sql(q3, conn)
print("\n[3] MONTHLY REVENUE TREND")
print(df_monthly.to_string(index=False))

fig3 = make_subplots(specs=[[{"secondary_y": True}]])
fig3.add_trace(go.Bar(x=df_monthly["month"], y=df_monthly["monthly_revenue_usd"],
                      name="Revenue (USD)", marker_color="#c45c2a", opacity=0.85))
fig3.add_trace(go.Scatter(x=df_monthly["month"], y=df_monthly["flights"],
                          name="Flights", mode="lines+markers",
                          line=dict(color="#2a7c6f", width=2)),
               secondary_y=True)
fig3.update_layout(title="Monthly Revenue and Flight Volume",
                   template="plotly_white", legend=dict(x=0.01, y=0.99))
fig3.update_yaxes(title_text="Revenue (USD)", secondary_y=False)
fig3.update_yaxes(title_text="Number of Flights", secondary_y=True)
fig3.write_html(f"{OUTPUT_DIR}/03_monthly_trend.html")

# ── 4. AIRLINE PERFORMANCE ────────────────────────────────────
q4 = """
SELECT
    al.airline_name,
    al.airline_type,
    COUNT(DISTINCT f.flight_id) AS flights,
    ROUND(100.0 * SUM(CASE WHEN f.actual_departure <= f.scheduled_departure THEN 1 ELSE 0 END)
          / COUNT(f.flight_id), 1) AS on_time_pct,
    ROUND(SUM(cs.revenue_usd), 0) AS total_revenue_usd
FROM flights f
JOIN airlines al ON f.airline_code = al.airline_code
JOIN cargo_shipments cs ON f.flight_id = cs.flight_id
GROUP BY al.airline_name
ORDER BY total_revenue_usd DESC
"""
df_airline = pd.read_sql(q4, conn)
print("\n[4] AIRLINE PERFORMANCE")
print(df_airline.to_string(index=False))

fig4 = px.scatter(df_airline, x="on_time_pct", y="total_revenue_usd",
                  size="flights", color="airline_type", text="airline_name",
                  title="Airline Performance: On-Time Rate vs Revenue",
                  labels={"on_time_pct": "On-Time Rate (%)",
                          "total_revenue_usd": "Total Revenue (USD)",
                          "airline_type": "Type"},
                  color_discrete_map={"Full Service": "#c45c2a", "Low Cost": "#2a7c6f"})
fig4.update_traces(textposition="top center")
fig4.update_layout(template="plotly_white")
fig4.write_html(f"{OUTPUT_DIR}/04_airline_performance.html")

# ── 5. COMPLAINT ANALYSIS ─────────────────────────────────────
q5 = """
SELECT
    c.complaint_type,
    COUNT(*) AS total_complaints,
    SUM(c.resolved) AS resolved,
    ROUND(100.0 * SUM(c.resolved) / COUNT(*), 1) AS resolution_rate_pct
FROM complaints c
GROUP BY c.complaint_type
ORDER BY total_complaints DESC
"""
df_complaints = pd.read_sql(q5, conn)
print("\n[5] COMPLAINT ANALYSIS")
print(df_complaints.to_string(index=False))

fig5 = px.bar(df_complaints, x="complaint_type", y=["total_complaints", "resolved"],
              title="Complaints by Type: Total vs Resolved",
              barmode="overlay",
              labels={"value": "Count", "complaint_type": "Complaint Type",
                      "variable": ""},
              color_discrete_map={"total_complaints": "#e8b49a", "resolved": "#c45c2a"})
fig5.update_layout(template="plotly_white")
fig5.write_html(f"{OUTPUT_DIR}/05_complaint_analysis.html")

# ── 6. LOAD FACTOR ────────────────────────────────────────────
q6 = """
SELECT
    a1.city || ' → ' || a2.city AS route,
    COUNT(DISTINCT f.flight_id) AS flights,
    ROUND(AVG(f.capacity_kg), 0) AS avg_capacity_kg,
    ROUND(AVG(rw.total_weight), 0) AS avg_loaded_kg,
    ROUND(100.0 * AVG(rw.total_weight) / AVG(f.capacity_kg), 1) AS load_factor_pct
FROM flights f
JOIN airports a1 ON f.origin = a1.airport_code
JOIN airports a2 ON f.destination = a2.airport_code
JOIN (SELECT flight_id, SUM(weight_kg) AS total_weight FROM cargo_shipments GROUP BY flight_id) rw
    ON f.flight_id = rw.flight_id
GROUP BY f.origin, f.destination
HAVING flights >= 5
ORDER BY load_factor_pct DESC
"""
df_load = pd.read_sql(q6, conn)
print("\n[6] LOAD FACTOR BY ROUTE")
print(df_load.to_string(index=False))

fig6 = px.bar(df_load, x="route", y="load_factor_pct",
              color="load_factor_pct", color_continuous_scale="RdYlGn",
              title="Cargo Load Factor by Route (%)",
              labels={"load_factor_pct": "Load Factor (%)", "route": "Route"})
fig6.add_hline(y=70, line_dash="dash", line_color="red",
               annotation_text="70% target", annotation_position="top right")
fig6.update_layout(template="plotly_white", coloraxis_showscale=False,
                   xaxis_tickangle=30)
fig6.write_html(f"{OUTPUT_DIR}/06_load_factor.html")

conn.close()

print("\n" + "=" * 60)
print("ANALYSIS COMPLETE")
print(f"Charts saved to /{OUTPUT_DIR}/")
print("=" * 60)

# Summary stats
print("\nKEY FINDINGS:")
top_route = df_routes.iloc[0]
print(f"  Highest revenue route: {top_route['route']} (${top_route['total_revenue_usd']:,.0f})")
top_cargo = df_cargo.iloc[0]
print(f"  Top cargo type by revenue: {top_cargo['cargo_type']} (${top_cargo['total_revenue_usd']:,.0f})")
best_load = df_load.iloc[0]
print(f"  Best load factor route: {best_load['route']} ({best_load['load_factor_pct']}%)")
total_complaints = df_complaints['total_complaints'].sum()
total_resolved = df_complaints['resolved'].sum()
print(f"  Overall complaint resolution rate: {100*total_resolved/total_complaints:.1f}%")
