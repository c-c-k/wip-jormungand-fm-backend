"""
TODO: DOC: tests/dataset.py
"""

from datetime import datetime, timedelta

from sqlalchemy import text, insert, select, exists

from jormungand.core.db import (
    UserRole, Tables, get_table_by_name)

DATASET_TEMPLATE = {
    'users': {
        'customer_user_1': {
            'id': 51,
            'user_role': int(UserRole.CUSTOMER),
            'username': 'customer_user_1',
            'password': 'pass',
            'email': 'customer_user_1@email_1.com',
            'avatar_url': 'user_avatars/customer_user_1.png',
        },
        'airline_user_1': {
            'id': 61,
            'user_role': int(UserRole.AIRLINE_COMPANY),
            'username': 'airline_user_1',
            'password': 'pass',
            'email': 'airline_user_1@email_1.com',
            'avatar_url': 'user_avatars/airline_user_1.png',
        },
        'admin_user_1': {
            'id': 71,
            'user_role': int(UserRole.ADMINISTRATOR),
            'username': 'admin_user_1',
            'password': 'pass',
            'email': 'admin_user_1@email_1.com',
            'avatar_url': 'user_avatars/admin_user_1.png',
        },
    },
    'countries': {
        'country_1': {
            'id': 61,
            'name': 'country_1',
            'flag_url': 'country_1.png',
        },
    },
    'airline_companies': {
        'airline_company_1': {
            'id': 61,
            'country_id': 61,
            'user_id': 61,
            'name': 'airline_company_1',
        },
    },
    'customers': {
        'customer_1': {
            'id': 51,
            'user_id': 51,
            'first_name': 'customer_1_first_name',
            'last_name': 'customer_1_last_name',
            'address': 'country A, city B, street C 5551',
            'phone_number': '111 111 1111111',
            'credit_card_number': '4000000000000010',
        },
    },
    'administrators': {
        'administrator_1': {
            'id': 71,
            'user_id': 71,
            'first_name': 'administrator_1_first_name',
            'last_name': 'administrator_1_last_name',
        },
    },
    'flights': {
        'flight_template_dt_now': {
            'id': 1,
            'airline_company_id': 61,
            'origin_country_id': 81,
            'destination_country_id': 881,
            'departure_time': datetime.now(),
            'landing_time': (datetime.now() + timedelta(hours=1)),
            'remaining_tickets': 40,
        },
    },
    'tickets': {
        'ticket_template': {
            'id': 1,
            'flight_id': 1,
            'customer_id': 51,
        },
    },
}
DATASET_VALID = {

    # USERS
    'users': {

        # CUSTOMER USERS
        'customer_user_1': {
            'id': 51,
            'user_role': UserRole.CUSTOMER.value,
            'username': 'customer_user_1',
            'password': 'pass',
            'email': 'customer_user_1@email_1.com',
            'avatar_url': 'user_avatars/customer_user_1.png',
        },
        'customer_user_2': {
            'id': 52,
            'user_role': UserRole.CUSTOMER.value,
            'username': 'customer_user_2',
            'password': 'pass',
            'email': 'customer_user_2@email_1.com',
            'avatar_url': 'user_avatars/customer_user_2.png',
        },

        # AIRLINE COMPANY USERS
        'airline_user_1': {
            'id': 61,
            'user_role': UserRole.CUSTOMER.value,
            'username': 'airline_user_1',
            'password': 'pass',
            'email': 'airline_user_1@email_1.com',
            'avatar_url': 'user_avatars/airline_user_1.png',
        },
        'airline_user_2': {
            'id': 62,
            'user_role': UserRole.CUSTOMER.value,
            'username': 'airline_user_2',
            'password': 'pass',
            'email': 'airline_user_2@email_1.com',
            'avatar_url': 'user_avatars/airline_user_2.png',
        },

        # ADMINISTRATOR USERS
        'admin_user_1': {
            'id': 71,
            'user_role': UserRole.CUSTOMER.value,
            'username': 'admin_user_1',
            'password': 'pass',
            'email': 'admin_user_1@email_1.com',
            'avatar_url': 'user_avatars/admin_user_1.png',
        },
        'admin_user_2': {
            'id': 72,
            'user_role': UserRole.CUSTOMER.value,
            'username': 'admin_user_2',
            'password': 'pass',
            'email': 'admin_user_2@email_1.com',
            'avatar_url': 'user_avatars/admin_user_2.png',
        },
    },

    # COUNTRIES
    'countries': {

        # AIRLINE COMPANY COUNTRIES
        'airline_country_1': {
            'id': 61,
            'name': 'airline_country_1',
            'flag_url': 'country_flags/airline_country_1.png',
        },
        'airline_country_2': {
            'id': 62,
            'name': 'airline_country_2',
            'flag_url': 'country_flags/airline_country_2.png',
        },

        # FLIGHT ORIGIN COUNTRIES
        'origin_country_1': {
            'id': 81,
            'name': 'origin_country_1',
            'flag_url': 'country_flags/origin_country_1.png',
        },
        'origin_country_2': {
            'id': 82,
            'name': 'origin_country_2',
            'flag_url': 'country_flags/origin_country_2.png',
        },

        # FLIGHT DESTINATION COUNTRIES
        'destination_country_1': {
            'id': 881,
            'name': 'destination_country_1',
            'flag_url': 'country_flags/destination_country_1.png',
        },
        'destination_country_2': {
            'id': 882,
            'name': 'destination_country_2',
            'flag_url': 'country_flags/destination_country_2.png',
        },
    },

    # AIRLINE COMPANIES
    'airline_companies': {
        'airline_company_1': {
            'id': 61,
            'country_id': 61,
            'user_id': 61,
            'name': 'airline_company_1',
        },
        'airline_company_2': {
            'id': 62,
            'country_id': 62,
            'user_id': 62,
            'name': 'airline_company_2',
        },
    },

    # CUSTOMERS
    'customers': {
        'customer_1': {
            'id': 51,
            'user_id': 51,
            'first_name': 'customer_1_first_name',
            'last_name': 'customer_1_last_name',
            'address': 'country A, city B, street C 5551',
            'phone_number': '111 111 1111111',
            'credit_card_number': '4000000000000010',
        },
        'customer_2': {
            'id': 52,
            'user_id': 52,
            'first_name': 'customer_2_first_name',
            'last_name': 'customer_2_last_name',
            'address': 'country A, city B, street C 5552',
            'phone_number': '222 222 2222222',
            'credit_card_number': '4000000000000028',
        },
    },

    # ADMINISTRATORS
    'administrators': {
        'administrator_1': {
            'id': 71,
            'user_id': 71,
            'first_name': 'administrator_1_first_name',
            'last_name': 'administrator_1_last_name',
        },
        'administrator_2': {
            'id': 72,
            'user_id': 72,
            'first_name': 'administrator_2_first_name',
            'last_name': 'administrator_2_last_name',
        },
    },

    # FLIGHTS
    'flights': {
        'flight_template_dt_now': {
            'id': 1,
            'airline_company_id': 61,
            'origin_country_id': 81,
            'destination_country_id': 881,
            'departure_time': datetime.now(),
            'landing_time': (datetime.now() + timedelta(hours=1)),
            'remaining_tickets': 40,
        },
    },

    # TICKETS
    'tickets': {
        'ticket_template': {
            'id': 1,
            'flight_id': 1,
            'customer_id': 51,
        },
    },

}

TABLE_DEPENDANCEY_ORDER = {
        'users': 1, 'countries': 2, 'airline_companies': 3,
        'customers': 4, 'administrators': 5, 'flights': 6, 'tickets': 7}

INSERTION_SQL = {    
    'users': text("""
    INSERT INTO users
        ( id, user_role, username, password, email, avatar_url )
    VALUES
        ( :id, :user_role, :username, :password, :email, :avatar_url )
    """),
    'countries': text("""
    INSERT INTO countries
        ( id, name, flag_url )
    VALUES
        ( :id, :name, :flag_url )
    """),
    'airline_companies': text("""
    INSERT INTO airline_companies
        ( id, country_id, user_id, name )
    VALUES
        ( :id, :country_id, :user_id, :name )
    """),
    'customers': text("""
    INSERT INTO customers
        ( id, user_id, first_name, last_name, address, phone_number,
        credit_card_number )
    VALUES
        ( :id, :user_id, :first_name, :last_name, :address, :phone_number,
        :credit_card_number )
    """),
    'administrators': text("""
    INSERT INTO administrators
        ( id, user_id, first_name, last_name )
    VALUES
        ( :id, :user_id, :first_name, :last_name )
    """),
    'flights': text("""
    INSERT INTO flights
        ( id, airline_company_id, origin_country_id,
        destination_country_id, departure_time, landing_time,
        remaining_tickets )
    VALUES
        ( :id, :airline_company_id, :origin_country_id,
        :destination_country_id, :departure_time, :landing_time,
        :remaining_tickets )
    """),
    'tickets': text("""
    INSERT INTO tickets
        ( id, flight_id, customer_id)
    VALUES
        ( :id, :flight_id, :customer_id)
    """)
}


def insert_dataset(connection, dataset: dict):
    sorted_table_names = sorted(
            dataset.keys(),
            key=lambda table_name: TABLE_DEPENDANCEY_ORDER[table_name])
    for table_name in sorted_table_names:
        connection.execute(INSERTION_SQL[table_name],
                           list(dataset[table_name].values()))


def setup_dataset(conn, dataset: dict):
    used_table_names = sorted(
            dataset.keys(),
            key=lambda t_name: Tables.t_names_sort_key[t_name])
    for table_name in used_table_names:
        table = get_table_by_name(table_name)
        conn.execute(
            insert(table), tuple(dataset[table_name].values()))


def compare_dataset_all(conn, dataset: dict):
    used_table_names = dataset.keys()
    for table_name in used_table_names:
        table = get_table_by_name(table_name)
        for entry in dataset[table_name].values():
            stmt = select(table).filter_by(**entry)
            result = conn.execute(stmt).all()
            assert len(result) == 1
