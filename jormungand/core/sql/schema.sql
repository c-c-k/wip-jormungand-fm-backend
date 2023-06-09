DROP TABLE IF EXISTS user_roles CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS customers CASCADE;
DROP TABLE IF EXISTS administrators CASCADE;
DROP TABLE IF EXISTS countries CASCADE;
DROP TABLE IF EXISTS airports CASCADE;
DROP TABLE IF EXISTS meta CASCADE;

DROP VIEW IF EXISTS airports_join_countries CASCADE;
DROP VIEW IF EXISTS airports_search_strings CASCADE;

CREATE TABLE user_roles (
    user_role_id smallserial PRIMARY KEY,
    role_name varchar(16) UNIQUE NOT NULL
);

CREATE TABLE users (
    user_id bigserial PRIMARY KEY,
    user_role_id smallint REFERENCES user_roles ON DELETE RESTRICT NOT NULL,
    username varchar(64) UNIQUE NOT NULL,
    password varchar(128) NOT NULL,
    email varchar(255) NOT NULL,
    avatar_url varchar(1023)
);

CREATE TABLE customers (
    user_id bigint PRIMARY KEY REFERENCES users ON DELETE CASCADE UNIQUE NOT NULL,
    first_name varchar(64),
    last_name varchar(64),
    address varchar(1023),
    phone_number varchar(20) UNIQUE,
    credit_card_number varchar(20) UNIQUE
);

CREATE TABLE administrators (
    user_id bigint PRIMARY KEY REFERENCES users ON DELETE CASCADE UNIQUE NOT NULL,
    first_name varchar(64),
    last_name varchar(64)
);

CREATE TABLE countries (
    country_id serial PRIMARY KEY,
    code varchar UNIQUE NOT NULL,
    name varchar UNIQUE NOT NULL
);

CREATE TABLE airports (
    airport_id serial PRIMARY KEY,
    country_id integer REFERENCES countries ON DELETE RESTRICT NOT NULL,
    iata_code varchar UNIQUE NOT NULL,
    name varchar,
    municipality varchar
);

CREATE TABLE meta (
    property varchar UNIQUE NOT NULL,
    value varchar
);

CREATE VIEW airports_join_countries
AS SELECT
    air.airport_id AS airport_id,
    cou.code AS country_code,
    air.iata_code AS iata_code,
    cou.name AS country_name,
    air.name AS airport_name,
    air.municipality AS municipality
FROM airports AS air
INNER JOIN countries AS cou USING (country_id);

CREATE VIEW airports_search_strings
AS SELECT
    country_code AS search_string,
    airport_id,
    1 AS priority
FROM airports_join_countries
UNION ALL
SELECT
    iata_code AS search_string,
    airport_id,
    2 AS priority
FROM airports_join_countries
UNION ALL
SELECT
    country_name AS search_string,
    airport_id,
    3 AS priority
FROM airports_join_countries
UNION ALL
SELECT
    municipality AS search_string,
    airport_id,
    4 AS priority
FROM airports_join_countries
UNION ALL
SELECT
    airport_name AS search_string,
    airport_id,
    5 AS priority
FROM airports_join_countries
ORDER BY
    priority ASC,
    search_string ASC;
