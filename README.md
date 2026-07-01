# Air Cargo Operations Analysis

**Tools:** Python · SQL (SQLite) · Pandas · Plotly  
**Domain:** Aviation / Logistics  
**Type:** Exploratory Data Analysis + Operational Insights

---

## Project Overview

This project analyses air cargo operations data to surface insights around route performance, revenue trends, cargo mix, airline efficiency, and service quality. The goal is to help operations and commercial teams make data-informed decisions around capacity planning, route prioritisation, and complaint reduction.

The analysis is built entirely on SQL queries run via Python, with results visualised using Plotly.

---

## Key Findings

| Metric | Finding |
|--------|---------|
| Highest revenue route | Hyderabad → Delhi ($3.0M) |
| Top cargo type by revenue | Pharmaceuticals ($10.2M, avg $12.28/kg) |
| Best load factor | Chennai → Singapore (44.8%) |
| Complaint resolution rate | 51.6% overall |
| Busiest month | December (88 flights, $3.38M revenue) |

---

## Business Questions Answered

1. **Which routes generate the most revenue?** — Top 10 routes ranked by total and per-shipment revenue
2. **Which cargo types are most profitable?** — Revenue share and rate per kg by cargo category
3. **How does revenue trend over time?** — Monthly revenue and flight volume across 2024
4. **Which airlines perform best?** — On-time rate vs revenue comparison across carriers
5. **Where are the operational bottlenecks?** — Complaint volume, type, and resolution rate
6. **Are we using capacity efficiently?** — Load factor analysis by route

---

## Project Structure

```
air-cargo-analysis/
│
├── data/
│   └── air_cargo.db          # SQLite database (800 flights, 2,814 shipments)
│
├── queries/
│   └── analysis_queries.sql  # All SQL queries used in the analysis
│
├── outputs/
│   ├── 01_top_routes_revenue.html
│   ├── 02_cargo_type_revenue.html
│   ├── 03_monthly_trend.html
│   ├── 04_airline_performance.html
│   ├── 05_complaint_analysis.html
│   └── 06_load_factor.html
│
├── generate_data.py           # Database generation script
├── air_cargo_analysis.py      # Main analysis script
└── README.md
```

---

## Database Schema

```sql
airports        -- Airport codes, cities, countries
airlines        -- Carrier details and type (Full Service / Low Cost)
flights         -- 800 flights with route, date, capacity, and delay info
cargo_shipments -- 2,814 shipments with weight, revenue, and cargo type
complaints      -- 246 complaints with type and resolution status
```

---

## How to Run

```bash
# Clone the repo
git clone https://github.com/Alekhya-Ghosh/air-cargo-analysis.git
cd air-cargo-analysis

# Install dependencies
pip install pandas plotly

# Generate the database
python generate_data.py

# Run the full analysis
python air_cargo_analysis.py
```

Charts are saved as interactive HTML files in the `outputs/` folder.

---

## Skills Demonstrated

- SQL query design (JOINs, aggregations, subqueries, CASE statements, window-style logic)
- Python-based ETL and analysis pipeline using Pandas
- Interactive data visualisation with Plotly
- Translating data findings into business recommendations
- Clean project structure and documentation

---

Built by Alekhya Ghosh | [LinkedIn](https://linkedin.com/in/alekhya-ghosh-0a9963248) 

