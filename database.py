# database.py

import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname='postgres',      # <-- Put your DB name here
        user='postgres',    # <-- DB username (e.g., postgres)
        password='Star@1237',# <-- DB password
        host='localhost',           # <-- Usually localhost
        port='5432'                 # <-- Default PostgreSQL port
    )
