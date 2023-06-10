DROP TABLE IF EXISTS airline_companies CASCADE;

DROP TABLE IF EXISTS flights CASCADE;

DROP TABLE IF EXISTS countries CASCADE;

DROP TABLE IF EXISTS tickets CASCADE;

CREATE TABLE countries (
    country_id integer PRIMARY KEY,
    code varchar(2) UNIQUE NOT NULL,
    name varchar(64) UNIQUE NOT NULL
);

CREATE TABLE airports (
    airport_id integer PRIMARY KEY,
    country_id integer REFERENCES countries ON DELETE RESTRICT NOT NULL,
    iata_code varchar UNIQUE NOT NULL,
    name varchar,
    municipality varchar,
    home_link varchar,
    wikipedia_link varchar
);

CREATE TABLE meta (
    property varchar UNIQUE NOT NULL,
    value varchar
);
