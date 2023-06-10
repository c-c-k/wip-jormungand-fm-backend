CREATE OR REPLACE PROCEDURE get_user_by_username(_username text)
    --Returns basic user info (*Users* table only), this should be used during user login.
LANGUAGE SQL
AS $$
    SELECT * FROM users WHERE username = _username;
$$;

CREATE OR REPLACE PROCEDURE get_airline_by_username(_username text)
    --Returns full airline info (join of *Airline_Companies* and *Users* tables).
LANGUAGE SQL
AS $$
    SELECT * FROM users
        INNER JOIN airline_companies ON (users.id = airline_companies.user_id)
    WHERE username = _username;
$$;

CREATE OR REPLACE PROCEDURE get_customer_by_username(_username text)
    --Returns full customer info (join of *Customers* and *Users* tables).
LANGUAGE SQL
AS $$
SELECT * FROM users
                  INNER JOIN customers ON (users.id = customers.user_id)
WHERE username = _username;
$$;

CREATE OR REPLACE PROCEDURE get_flights_by_parameters(
        _origin_country_id int, _destination_country_id int, _date date)
    --Returns a list of all flights answering the input parameters of origin, destination and date.
LANGUAGE SQL
AS $$
    SELECT * FROM flights
    WHERE
        (origin_country_id = _origin_country_id)
        AND (destination_country_id = _destination_country_id)
        AND (departure_time = _date)
$$;

CREATE OR REPLACE PROCEDURE get_flights_by_airline_id(_airline_id bigint)
    --Returns a list of all flights belonging to airline company of the input id.
LANGUAGE SQL
AS $$
SELECT * FROM flights WHERE airline_company_id = _airline_id
$$;

CREATE OR REPLACE PROCEDURE get_arrival_flights(_country_id int)
    --Returns a list of all flights scheduled to land in the country of the input id in the next 12 hours.
LANGUAGE SQL
AS $$
SELECT * FROM flights
WHERE
  (destination_country_id = _country_id)
  AND (landing_time >= current_timestamp)
  AND (landing_time <= (current_timestamp + make_interval(hours=>12)))
$$;

CREATE OR REPLACE PROCEDURE get_departure_flights(_country_id int)
    --Returns a list of all flights scheduled to take off from the country of the input id in the next 12 hours.
LANGUAGE SQL
AS $$
SELECT * FROM flights
WHERE
    (origin_country_id = _country_id)
  AND (landing_time >= current_timestamp)
  AND (landing_time <= (current_timestamp + make_interval(hours=>12)))
$$;

CREATE OR REPLACE PROCEDURE get_tickets_by_customer(_customer_id bigint)
    --Returns a list of all the tickets purchased by the customer of the input id.
LANGUAGE SQL
AS $$
    SELECT * FROM tickets WHERE customer_id = _customer_id
$$;


