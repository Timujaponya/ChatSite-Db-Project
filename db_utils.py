# db_utils.py
from db_connection import get_connection
from sql_queries import QUERIES

def execute_query(query_name, params=None, fetch_one=False, fetch_all=False):
    query = QUERIES.get(query_name)
    if not query:
        raise ValueError(f"Query '{query_name}' not found.")
    
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params or [])
            if fetch_one:
                return cursor.fetchone()
            if fetch_all:
                return cursor.fetchall()
            conn.commit()
            return None
