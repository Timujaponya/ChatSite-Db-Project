# db_connection.py
import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname="db_twit",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )
