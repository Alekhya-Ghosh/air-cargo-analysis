import sqlite3
import pandas as pd
import random
from datetime import datetime, timedelta

random.seed(42)

# Reference data
airports = [
    ("DEL", "Indira Gandhi International", "Delhi", "India"),
    ("BOM", "Chhatrapati Shivaji International", "Mumbai", "India"),
    ("BLR", "Kempegowda International", "Bangalore", "India"),
    ("MAA", "Chennai International", "Chennai", "India"),
    ("CCU", "Netaji Subhas Chandra Bose", "Kolkata", "India"),
    ("HYD", "Rajiv Gandhi International", "Hyderabad", "India"),
    ("DXB", "Dubai International", "Dubai", "UAE"),
    ("SIN", "Changi Airport", "Singapore", "Singapore"),
    ("LHR", "Heathrow Airport", "London", "UK"),
    ("FRA", "Frankfurt Airport", "Frankfurt", "Germany"),
]

airlines = [
    ("AI", "Air India", "Full Service"),
    ("6E", "IndiGo", "Low Cost"),
    ("SG", "SpiceJet", "Low Cost"),
    ("UK", "Vistara", "Full Service"),
    ("EK", "Emirates", "Full Service"),
]

cargo_types = ["General Freight", "Perishables", "Pharmaceuticals", "Electronics", "Automotive Parts", "Textiles"]

routes = [
    ("DEL", "BOM"), ("DEL", "BLR"), ("DEL", "MAA"), ("DEL", "DXB"),
    ("BOM", "BLR"), ("BOM", "SIN"), ("BOM", "LHR"),
    ("BLR", "SIN"), ("BLR", "FRA"), ("CCU", "DEL"),
    ("HYD", "DEL"), ("HYD", "BOM"), ("MAA", "SIN"),
]

conn = sqlite3.connect(r"C:\Users\ALEKHYA GHOSH\PycharmProjects\Air-Cargo-Analysis\air-cargo-analysis\data\air_cargo.db")
c = conn.cursor()

c.executescript("""
DROP TABLE IF EXISTS airports;
DROP TABLE IF EXISTS airlines;
DROP TABLE IF EXISTS flights;
DROP TABLE IF EXISTS cargo_shipments;
DROP TABLE IF EXISTS complaints;

CREATE TABLE airports (
    airport_code TEXT PRIMARY KEY,
    airport_name TEXT,
    city TEXT,
    country TEXT
);

CREATE TABLE airlines (
    airline_code TEXT PRIMARY KEY,
    airline_name TEXT,
    airline_type TEXT
);

CREATE TABLE flights (
    flight_id INTEGER PRIMARY KEY AUTOINCREMENT,
    flight_number TEXT,
    airline_code TEXT,
    origin TEXT,
    destination TEXT,
    departure_date DATE,
    scheduled_departure TEXT,
    actual_departure TEXT,
    capacity_kg REAL,
    FOREIGN KEY (airline_code) REFERENCES airlines(airline_code),
    FOREIGN KEY (origin) REFERENCES airports(airport_code),
    FOREIGN KEY (destination) REFERENCES airports(airport_code)
);

CREATE TABLE cargo_shipments (
    shipment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    flight_id INTEGER,
    cargo_type TEXT,
    weight_kg REAL,
    revenue_usd REAL,
    booking_date DATE,
    FOREIGN KEY (flight_id) REFERENCES flights(flight_id)
);

CREATE TABLE complaints (
    complaint_id INTEGER PRIMARY KEY AUTOINCREMENT,
    flight_id INTEGER,
    complaint_type TEXT,
    complaint_date DATE,
    resolved INTEGER,
    FOREIGN KEY (flight_id) REFERENCES flights(flight_id)
);
""")

# Insert reference data
c.executemany("INSERT INTO airports VALUES (?,?,?,?)", airports)
c.executemany("INSERT INTO airlines VALUES (?,?,?)", airlines)

# Generate flights
start_date = datetime(2024, 1, 1)
flight_records = []
for i in range(800):
    origin, dest = random.choice(routes)
    airline = random.choice(airlines)[0]
    dep_date = start_date + timedelta(days=random.randint(0, 364))
    sched_hour = random.randint(5, 22)
    delay_min = random.choices([0, random.randint(15,240)], weights=[0.7, 0.3])[0]
    actual_hour = sched_hour + delay_min // 60
    capacity = random.choice([5000, 10000, 15000, 20000, 30000])
    flight_records.append((
        f"{airline}{random.randint(100,999)}",
        airline, origin, dest,
        dep_date.strftime("%Y-%m-%d"),
        f"{sched_hour:02d}:00",
        f"{actual_hour:02d}:{delay_min%60:02d}",
        capacity
    ))

c.executemany("""INSERT INTO flights 
    (flight_number, airline_code, origin, destination, departure_date, scheduled_departure, actual_departure, capacity_kg)
    VALUES (?,?,?,?,?,?,?,?)""", flight_records)

# Generate shipments
rate_map = {"General Freight": 3.5, "Perishables": 5.2, "Pharmaceuticals": 12.0,
            "Electronics": 8.5, "Automotive Parts": 4.0, "Textiles": 2.8}

shipment_records = []
for flight_id in range(1, 801):
    n_shipments = random.randint(1, 6)
    capacity = flight_records[flight_id-1][7]
    remaining = capacity
    for _ in range(n_shipments):
        if remaining < 100:
            break
        ctype = random.choice(cargo_types)
        weight = round(random.uniform(100, min(remaining * 0.4, 5000)), 1)
        revenue = round(weight * rate_map[ctype] * random.uniform(0.85, 1.2), 2)
        remaining -= weight
        book_days_before = random.randint(1, 30)
        dep_date = datetime.strptime(flight_records[flight_id-1][4], "%Y-%m-%d")
        book_date = (dep_date - timedelta(days=book_days_before)).strftime("%Y-%m-%d")
        shipment_records.append((flight_id, ctype, weight, revenue, book_date))

c.executemany("INSERT INTO cargo_shipments (flight_id, cargo_type, weight_kg, revenue_usd, booking_date) VALUES (?,?,?,?,?)",
              shipment_records)

# Generate complaints
complaint_types = ["Delayed Delivery", "Damaged Cargo", "Documentation Error", "Weight Discrepancy", "Handling Issue"]
complaint_records = []
for flight_id in range(1, 801):
    if random.random() < 0.22:
        n = random.randint(1, 2)
        for _ in range(n):
            dep_date = datetime.strptime(flight_records[flight_id-1][4], "%Y-%m-%d")
            comp_date = (dep_date + timedelta(days=random.randint(0,5))).strftime("%Y-%m-%d")
            complaint_records.append((
                flight_id,
                random.choice(complaint_types),
                comp_date,
                random.randint(0, 1)
            ))

c.executemany("INSERT INTO complaints (flight_id, complaint_type, complaint_date, resolved) VALUES (?,?,?,?)",
              complaint_records)

conn.commit()
conn.close()
print(f"Database created: {len(flight_records)} flights, {len(shipment_records)} shipments, {len(complaint_records)} complaints")
