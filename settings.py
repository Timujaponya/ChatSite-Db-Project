# settings.py
from db_utils import execute_query

def add_user(username, email, password):
    return execute_query('insert_user', (username, email, password), fetch_one=True)

def authenticate_user(username, password):
    result = execute_query('authenticate_user', (username, password), fetch_one=True)
    return result is not None

def update_user(user_id, username, email):
    execute_query('update_user', (username, email, user_id))
    return f"User {user_id} updated."

def update_password(user_id, new_password):
    execute_query('update_password', (new_password, user_id))
    return f"Password for user {user_id} updated."

def update_profile_picture(user_id, profile_picture_path):
    execute_query('update_profile_picture', (profile_picture_path, user_id))
    return f"Profile picture for user {user_id} updated."

def get_user_id_by_username(username):
    result = execute_query('get_user_id_by_username', (username,), fetch_one=True)
    return result[0] if result else None

def get_user_profile(user_id):
    result = execute_query('select_user_profile', (user_id,), fetch_one=True)
    return result