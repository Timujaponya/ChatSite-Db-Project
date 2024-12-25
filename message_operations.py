# message_operations.py
from db_utils import execute_query

def add_message(user_id, content, server_id):
    return execute_query('insert_message', (user_id, content, server_id), fetch_one=True)

def list_messages(user_id):
    return execute_query('select_messages', (user_id,), fetch_all=True)

def list_all_messages_with_usernames(server_id):
    return execute_query('select_all_messages_with_usernames', (server_id,), fetch_all=True)

def delete_message(message_id):
    print(f"Executing delete_message with ID: {message_id}")  # Hata ayıklama için log ekleyin
    result = execute_query('delete_message', (message_id,))
    print(f"Delete result: {result}")  # Hata ayıklama için log ekleyin
    return result

def delete_messages_by_server(server_id):
    print(f"Executing delete_messages_by_server with server ID: {server_id}")  # Hata ayıklama için log ekleyin
    result = execute_query('delete_messages_by_server', (server_id,))
    print(f"Delete result: {result}")  # Hata ayıklama için log ekleyin
    return result

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

def add_server(server_name):
    return execute_query('insert_server', (server_name,), fetch_one=True)

def list_servers():
    return execute_query('select_servers', fetch_all=True)

def delete_server(server_id):
    print(f"Executing delete_server with ID: {server_id}")  # Hata ayıklama için log ekleyin
    delete_messages_by_server(server_id)  # Sunucuya bağlı tüm mesajları sil
    result = execute_query('delete_server', (server_id,))
    print(f"Delete result: {result}")  # Hata ayıklama için log ekleyin
    return result

def update_server(server_id, server_name):
    execute_query('update_server', (server_name, server_id))
    return f"Server {server_id} updated."

# Direct Messages
def add_dm(sender_id, receiver_id, content):
    return execute_query('insert_dm', (sender_id, receiver_id, content), fetch_one=True)

def list_dms(sender_id, receiver_id):
    return execute_query('select_dms', (receiver_id, sender_id), fetch_all=True)

def list_dm_conversations(user_id):
    return execute_query('list_dm_conversations', (user_id, user_id, user_id), fetch_all=True)

def delete_dm(dm_id):
    return execute_query('delete_dm', (dm_id,))