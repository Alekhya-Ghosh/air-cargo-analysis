Air Cargo Operations Analysis

Tools: Python · SQL (SQLite) · Pandas · Plotly  
Domain: Aviation / Logistics  
Type: Exploratory Data Analysis + Operational Insights

Project Overview

This project analyses air cargo operations data to surface insights around route performance, revenue trends, cargo mix, airline efficiency, and service quality. The goal is to help operations and commercial teams make data-informed decisions around capacity planning, route prioritisation, and complaint reduction.

The analysis is built entirely on SQL queries run via Python, with results visualised using Plotly.

Key Findings

| Metric | Finding |
|--------|---------|
| Highest revenue route | Hyderabad → Delhi ($3.0M) |
| Top cargo type by revenue | Pharmaceuticals ($10.2M, avg $12.28/kg) |
| Best load factor | Chennai → Singapore (44.8%) |
| Complaint resolution rate | 51.6% overall |
| Busiest month | December (88 flights, $3.38M revenue) |

## Business Questions Answered

1. Which routes generate the most revenue?
2. Which cargo types are most profitable?
3. How does revenue trend over time?
4. Which airlines perform best?
5. Where are the operational bottlenecks?
6. Are we using capacity efficiently?

Project Structure
air-cargo-analysis/

├── data/

│   └── air_cargo.db

├── queries/

│   └── analysis_queries.sql

├── outputs/

│   └── (6 interactive HTML charts)

├── generate_data.py

├── air_cargo_analysis.py

└── README.md

How to Run
pip install pandas plotly

python generate_data.py

python air_cargo_analysis.py

Skills Demonstrated

- SQL query design (JOINs, aggregations, subqueries, CASE statements)
- Python based ETL and analysis pipeline using Pandas
- Interactive data visualisation with Plotly
- Translating data findings into business recommendations
