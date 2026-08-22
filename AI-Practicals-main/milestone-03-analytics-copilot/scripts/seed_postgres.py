#!/usr/bin/env python3
"""
Seed milestone_3 (or any DB in DATABASE_URL) with sample SQL agent data.

Usage:
  python scripts/seed_postgres.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import psycopg2

from app.core.config import postgres_dsn

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS customers (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    unit_price NUMERIC(10, 2) NOT NULL
);

CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL REFERENCES customers(id),
    order_date DATE NOT NULL DEFAULT CURRENT_DATE,
    status TEXT NOT NULL DEFAULT 'completed'
);

CREATE TABLE IF NOT EXISTS order_items (
    id SERIAL PRIMARY KEY,
    order_id INT NOT NULL REFERENCES orders(id),
    product_id INT NOT NULL REFERENCES products(id),
    quantity INT NOT NULL CHECK (quantity > 0),
    line_total NUMERIC(12, 2) NOT NULL
);
"""


def seed():
    dsn = postgres_dsn()
    print(f"Connecting to database...")
    conn = psycopg2.connect(dsn)
    conn.autocommit = False
    try:
        with conn.cursor() as cur:
            cur.execute(SCHEMA_SQL)

            cur.execute("SELECT COUNT(*) FROM customers")
            if cur.fetchone()[0] > 0:
                print("Tables already contain data — skipping seed (delete rows to re-seed).")
                conn.commit()
                return

            cur.executemany(
                "INSERT INTO customers (name, email) VALUES (%s, %s)",
                [
                    ("Alice Johnson", "alice@example.com"),
                    ("Bob Smith", "bob@example.com"),
                    ("Carol Lee", "carol@example.com"),
                    ("Diana Prince", "diana@example.com"),
                ],
            )
            cur.executemany(
                "INSERT INTO products (name, category, unit_price) VALUES (%s, %s, %s)",
                [
                    ("Wireless Mouse", "electronics", 29.99),
                    ("Desk Lamp", "home", 45.00),
                    ("Notebook Pack", "office", 12.50),
                    ("USB-C Hub", "electronics", 59.99),
                    ("Ergonomic Chair", "office", 299.00),
                ],
            )
            cur.executemany(
                "INSERT INTO orders (customer_id, order_date, status) VALUES (%s, %s, %s)",
                [
                    (1, "2025-01-10", "completed"),
                    (2, "2025-02-05", "completed"),
                    (1, "2025-03-01", "pending"),
                    (3, "2025-03-15", "completed"),
                    (4, "2025-04-01", "completed"),
                ],
            )
            cur.executemany(
                "INSERT INTO order_items (order_id, product_id, quantity, line_total) VALUES (%s, %s, %s, %s)",
                [
                    (1, 1, 2, 59.98),
                    (1, 3, 1, 12.50),
                    (2, 2, 1, 45.00),
                    (3, 1, 1, 29.99),
                    (4, 4, 1, 59.99),
                    (4, 5, 1, 299.00),
                    (5, 3, 3, 37.50),
                ],
            )
        conn.commit()
        print("Seed completed: customers, products, orders, order_items populated.")
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    seed()
