# settings.py
from db_utils import execute_query
from werkzeug.security import generate_password_hash, check_password_hash

def add_user(username, email, password, role='user', description=''):
    hashed_password = generate_password_hash(password)
    return execute_query('insert_user', (username, email, hashed_password, role, description), fetch_one=True)

def authenticate_user(username, password):
    result = execute_query('authenticate_user', (username,), fetch_one=True)
    if result:
        stored_password, role = result
        if check_password_hash(stored_password, password):
            return role
    return None

def update_user(user_id, username=None, email=None, role=None, description=None):
    if username is not None and email is not None:
        execute_query('update_user', (username, email, role, description, user_id))
    elif role is not None:
        execute_query('update_user_role', (role, user_id))
    return f"User {user_id} updated."

def update_password(user_id, new_password):
    hashed_password = generate_password_hash(new_password)
    execute_query('update_password', (hashed_password, user_id))
    return f"Password for user {user_id} updated."

def update_profile_picture(user_id, profile_picture_path):
    execute_query('update_profile_picture', (profile_picture_path, user_id))
    return f"Profile picture for user {user_id} updated."

def update_user_description(user_id, description):
    execute_query('update_user_description', (description, user_id))
    return f"Description for user {user_id} updated."

def get_user_id_by_username(username):
    result = execute_query('get_user_id_by_username', (username,), fetch_one=True)
    return result[0] if result else None

def get_user_profile(user_id):
    result = execute_query('select_user_profile', (user_id,), fetch_one=True)
    return result