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
    country_id integer PRIMARY KEY,
    code varchar UNIQUE NOT NULL,
    name varchar UNIQUE NOT NULL
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
