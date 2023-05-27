"""
TODO: DOC: tests/dataset.py
"""

from datetime import datetime, timedelta

from jormungand.dal.ddl import UserRole

DATASET_VALID = {

    # USERS
    'users': {

        # CUSTOMER USERS
        'customer_user_1': {
            'id': 51,
            'user_role': UserRole.CUSTOMER,
            'username': 'customer_user_1',
            'password': 'pass',
            'email': 'customer_user_1@email_1.com',
            'avatar_url': 'user_avatars/customer_user_1.png',
        },
        'customer_user_2': {
            'id': 52,
            'user_role': UserRole.CUSTOMER,
            'username': 'customer_user_2',
            'password': 'pass',
            'email': 'customer_user_2@email_1.com',
            'avatar_url': 'user_avatars/customer_user_2.png',
        },

        # AIRLINE COMPANY USERS
        'airline_user_1': {
            'id': 61,
            'user_role': UserRole.CUSTOMER,
            'username': 'airline_user_1',
            'password': 'pass',
            'email': 'airline_user_1@email_1.com',
            'avatar_url': 'user_avatars/airline_user_1.png',
        },
        'airline_user_2': {
            'id': 62,
            'user_role': UserRole.CUSTOMER,
            'username': 'airline_user_2',
            'password': 'pass',
            'email': 'airline_user_2@email_1.com',
            'avatar_url': 'user_avatars/airline_user_2.png',
        },

        # ADMINISTRATOR USERS
        'admin_user_1': {
            'id': 71,
            'user_role': UserRole.CUSTOMER,
            'username': 'admin_user_1',
            'password': 'pass',
            'email': 'admin_user_1@email_1.com',
            'avatar_url': 'user_avatars/admin_user_1.png',
        },
        'admin_user_2': {
            'id': 72,
            'user_role': UserRole.CUSTOMER,
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
DATASET_INVALID = {
}
