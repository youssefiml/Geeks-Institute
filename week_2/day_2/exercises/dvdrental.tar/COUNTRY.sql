CREATE TABLE countries (
    country_id SERIAL PRIMARY KEY,
    countrname VARCHAR(100) UNIQUE NOT NULL,
    capital VARCHAR(100),
    flag TEXT,
    subregion VARCHAR(100),
    population BIGINT
);
