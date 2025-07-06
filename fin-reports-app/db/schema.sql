-- SQL para crear tablas básicas
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);

CREATE TABLE assets (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    symbol VARCHAR(20) UNIQUE NOT NULL
);

CREATE TABLE prices (
    id SERIAL PRIMARY KEY,
    asset_id INTEGER REFERENCES assets(id),
    date DATE NOT NULL,
    close NUMERIC,
    volume BIGINT
);
