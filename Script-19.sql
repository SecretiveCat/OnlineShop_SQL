create database assignment_02;



DROP TABLE IF EXISTS clients CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS orders CASCADE;


CREATE TABLE clients (
    id UUID PRIMARY KEY,
    name VARCHAR(100),
    surname VARCHAR(100),
    email VARCHAR(150),
    phone VARCHAR(50),
    address TEXT,
    status VARCHAR(20)
);

CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(255),
    product_category VARCHAR(100),
    description TEXT
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    order_date TIMESTAMP,
    client_id UUID REFERENCES clients(id),
    product_id INT REFERENCES products(product_id)
);



