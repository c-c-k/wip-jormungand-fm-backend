DROP TABLE IF EXISTS user_roles CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS airline_companies CASCADE;
DROP TABLE IF EXISTS customers CASCADE;
DROP TABLE IF EXISTS administrators CASCADE;
DROP TABLE IF EXISTS flights CASCADE;
DROP TABLE IF EXISTS countries CASCADE;
DROP TABLE IF EXISTS tickets CASCADE;

CREATE TABLE user_roles (
  id  smallserial PRIMARY KEY,
  role_name varchar(16) UNIQUE NOT NULL
);

CREATE TABLE users (
  id  bigserial PRIMARY KEY,
  user_role  smallint REFERENCES user_roles ON DELETE RESTRICT NOT NULL,
  username varchar(64) UNIQUE NOT NULL,
  password varchar(128) NOT NULL,
  email varchar(255) NOT NULL,
  avatar_url varchar(1023)
);

CREATE TABLE countries (
  id  smallserial PRIMARY KEY,
  name varchar(64) NOT NULL,
  flag_url varchar(1023)
);

CREATE TABLE airline_companies (
  id  bigserial PRIMARY KEY,
  country_id  smallint REFERENCES countries ON DELETE RESTRICT NOT NULL,
  user_id  bigint REFERENCES users ON DELETE RESTRICT UNIQUE NOT NULL,
  name varchar(64) UNIQUE NOT NULL
);

CREATE TABLE customers (
  id  bigserial PRIMARY KEY,
  user_id  bigint REFERENCES users ON DELETE RESTRICT UNIQUE NOT NULL,
  first_name varchar(64),
  last_name varchar(64),
  address varchar(1023),
  phone_number varchar(20) UNIQUE,
  credit_card_number varchar(20) UNIQUE
);

CREATE TABLE administrators (
  id  bigserial PRIMARY KEY,
  user_id  bigint REFERENCES users ON DELETE RESTRICT UNIQUE NOT NULL,
  first_name varchar(64),
  last_name varchar(64)
);

CREATE TABLE flights (
  id  bigserial PRIMARY KEY,
  airline_company_id  bigint REFERENCES airline_companies ON DELETE RESTRICT NOT NULL,
  origin_country_id  smallint REFERENCES countries ON DELETE RESTRICT NOT NULL,
  destination_country_id  smallint REFERENCES countries ON DELETE RESTRICT NOT NULL,
  departure_time timestamp,
  landing_time timestamp,
  remaining_tickets smallint
);

CREATE TABLE tickets (
  id  bigserial PRIMARY KEY,
  flight_id  bigint REFERENCES flights ON DELETE RESTRICT NOT NULL,
  customer_id  bigint REFERENCES customers ON DELETE RESTRICT NOT NULL,
  UNIQUE (flight_id, customer_id)
);

