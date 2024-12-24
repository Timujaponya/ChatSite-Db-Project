# user_operations.py
from db_utils import execute_query

def add_user(username, email, password, role='user'):
    return execute_query('insert_user', (username, email, password, role), fetch_one=True)

def list_users():
    return execute_query('select_users', fetch_all=True)

def delete_user(user_id):
    execute_query('delete_user', (user_id,))
    return f"User {user_id} deleted."

def update_user(user_id, username=None, email=None, role=None):
    if username is not None and email is not None:
        execute_query('update_user', (username, email, role, user_id))
    elif role is not None:
        execute_query('update_user_role', (role, user_id))
    return f"User {user_id} updated."

def authenticate_user(username, password):
    result = execute_query('authenticate_user', (username, password), fetch_one=True)
    return result is not None

def get_user_id_by_username(username):
    result = execute_query('get_user_id_by_username', (username,), fetch_one=True)
    return result[0] if result else None