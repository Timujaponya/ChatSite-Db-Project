# message_operations.py
from db_utils import execute_query

def add_message(user_id, content):
    return execute_query('insert_message', (user_id, content), fetch_one=True)

def list_messages(user_id):
    return execute_query('select_messages', (user_id,), fetch_all=True)

def list_all_messages_with_usernames():
    return execute_query('select_all_messages_with_usernames', fetch_all=True)

def delete_message(message_id):
    execute_query('delete_message', (message_id,))
    return f"Message {message_id} deleted."

def update_message(message_id, content):
    execute_query('update_message', (content, message_id))
    return f"Message {message_id} updated."

def like_message(message_id, user_id):
    execute_query('like_message', (message_id, user_id))
    return f"User {user_id} liked message {message_id}."

def unlike_message(message_id, user_id):
    execute_query('unlike_message', (message_id, user_id))
    return f"User {user_id} unliked message {message_id}."

def count_likes(message_id):
    result = execute_query('count_likes', (message_id,), fetch_one=True)
    return result[0] if result else 0