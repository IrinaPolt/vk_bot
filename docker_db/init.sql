CREATE DATABASE "${POSTGRES_DB}";

CREATE TABLE cakes (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    description VARCHAR(200),
    image VARCHAR(50),
    link VARCHAR(100),
    price FLOAT
);

CREATE TABLE ice_cream (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    description VARCHAR(200),
    image VARCHAR(50),
    link VARCHAR(100),
    price FLOAT
);

CREATE TABLE pastries (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    description VARCHAR(200),
    image VARCHAR(50),
    link VARCHAR(100),
    price FLOAT
);

\copy cakes(name, description, image, link, price) FROM '/docker-entrypoint-initdb.d/cakes.csv' WITH (FORMAT csv, HEADER true);
\copy ice_cream(name, description, image, link, price) FROM '/docker-entrypoint-initdb.d/ice_cream.csv' WITH (FORMAT csv, HEADER true);
\copy pastries(name, description, image, link, price) FROM '/docker-entrypoint-initdb.d/pastries.csv' WITH (FORMAT csv, HEADER true);