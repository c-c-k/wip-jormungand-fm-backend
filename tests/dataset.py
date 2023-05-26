"""
TODO: DOC: tests/dataset.py
"""

from jormungand.dal.ddl import UserRole

DATASET = {
    'users': {
        'customer_user_1': {
            'id': 551,
            'user_role': UserRole.CUSTOMER,
            'username': 'customer_user_1',
            'password': 'pass',
            'email': 'customer_user_1@email_1.com',
            'avatar_url': 'user_avatars/customer_user_1.png',
        },
        'customer_user_2': {
            'id': 552,
            'user_role': UserRole.CUSTOMER,
            'username': 'customer_user_2',
            'password': 'pass',
            'email': 'customer_user_2@email_1.com',
            'avatar_url': 'user_avatars/customer_user_2.png',
        },
        'airline_user_1': {
            'id': 561,
            'user_role': UserRole.CUSTOMER,
            'username': 'airline_user_1',
            'password': 'pass',
            'email': 'airline_user_1@email_1.com',
            'avatar_url': 'user_avatars/airline_user_1.png',
        },
        'airline_user_2': {
            'id': 562,
            'user_role': UserRole.CUSTOMER,
            'username': 'airline_user_2',
            'password': 'pass',
            'email': 'airline_user_2@email_1.com',
            'avatar_url': 'user_avatars/airline_user_2.png',
        },
        'admin_user_1': {
            'id': 571,
            'user_role': UserRole.CUSTOMER,
            'username': 'admin_user_1',
            'password': 'pass',
            'email': 'admin_user_1@email_1.com',
            'avatar_url': 'user_avatars/admin_user_1.png',
        },
        'admin_user_2': {
            'id': 572,
            'user_role': UserRole.CUSTOMER,
            'username': 'admin_user_2',
            'password': 'pass',
            'email': 'admin_user_2@email_1.com',
            'avatar_url': 'user_avatars/admin_user_2.png',
        },
    },
    'countries': {
        'airline_country_1': {
            'id': 5561,
            'name': 'airline_country_1',
            'flag_url': 'country_flags/airline_country_1.png',
        },
        'airline_country_2': {
            'id': 5562,
            'name': 'airline_country_2',
            'flag_url': 'country_flags/airline_country_2.png',
        },
        'origin_country_1': {
            'id': 651,
            'name': 'origin_country_1',
            'flag_url': 'country_flags/origin_country_1.png',
        },
        'origin_country_2': {
            'id': 652,
            'name': 'origin_country_2',
            'flag_url': 'country_flags/origin_country_2.png',
        },
        'destination_country_1': {
            'id': 651,
            'name': 'destination_country_1',
            'flag_url': 'country_flags/destination_country_1.png',
        },
        'destination_country_2': {
            'id': 652,
            'name': 'destination_country_2',
            'flag_url': 'country_flags/destination_country_2.png',
        },
    },
    'airline_companies': {
        'airline_company_1': {
            'id': 55561,
            'country_id': 5561,
            'user_id': 561,
            'name': 'airline_company_1',
        },
        'airline_company_2': {
            'id': 55562,
            'country_id': 5562,
            'user_id': 562,
            'name': 'airline_company_2',
        },
    },
    'customers': {
        'customer_1': {
            'id': ,
            'user_id': ,
            'first_name': '',
            'last_name': '',
            'address': '',
            'phone_number': '',
            'credit_card_number': '',
        },
    },

}
