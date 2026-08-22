-- Runs once on first Postgres container start (docker-entrypoint-initdb.d)

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

INSERT INTO customers (name, email) VALUES
    ('Alice Johnson', 'alice@example.com'),
    ('Bob Smith', 'bob@example.com'),
    ('Carol Lee', 'carol@example.com'),
    ('Diana Prince', 'diana@example.com');

INSERT INTO products (name, category, unit_price) VALUES
    ('Wireless Mouse', 'electronics', 29.99),
    ('Desk Lamp', 'home', 45.00),
    ('Notebook Pack', 'office', 12.50),
    ('USB-C Hub', 'electronics', 59.99),
    ('Ergonomic Chair', 'office', 299.00);

INSERT INTO orders (customer_id, order_date, status) VALUES
    (1, '2025-01-10', 'completed'),
    (2, '2025-02-05', 'completed'),
    (1, '2025-03-01', 'pending'),
    (3, '2025-03-15', 'completed'),
    (4, '2025-04-01', 'completed');

INSERT INTO order_items (order_id, product_id, quantity, line_total) VALUES
    (1, 1, 2, 59.98),
    (1, 3, 1, 12.50),
    (2, 2, 1, 45.00),
    (3, 1, 1, 29.99),
    (4, 4, 1, 59.99),
    (4, 5, 1, 299.00),
    (5, 3, 3, 37.50);
