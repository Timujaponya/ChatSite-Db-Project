# sql_queries.py
QUERIES = {
    # Users
    'insert_user': "INSERT INTO Users (username, email, password, role, description) VALUES (%s, %s, %s, %s, %s) RETURNING user_id;",
    'select_users': "SELECT * FROM Users;",
    'delete_user': "DELETE FROM Users WHERE user_id = %s;",
    'update_user': "UPDATE Users SET username = %s, email = %s, role = %s, description = %s WHERE user_id = %s;",
    'update_user_role': "UPDATE Users SET role = %s WHERE user_id = %s;",
    'authenticate_user': "SELECT password, role FROM Users WHERE username = %s;",  
    'get_user_id_by_username': "SELECT user_id FROM Users WHERE username = %s;",
    'select_user_profile': "SELECT user_id, username, email, profile_picture, role, description FROM Users WHERE user_id = %s;",
    'update_profile_picture': "UPDATE Users SET profile_picture = %s WHERE user_id = %s;",
    'update_user_description': "UPDATE Users SET description = %s WHERE user_id = %s;",

    # Servers
    'insert_server': "INSERT INTO Servers (server_name) VALUES (%s) RETURNING server_id;",
    'select_servers': "SELECT * FROM Servers;",
    'delete_server': "DELETE FROM Servers WHERE server_id = %s;",
    'update_server': "UPDATE Servers SET server_name = %s WHERE server_id = %s;",

    # Messages
    'insert_message': "INSERT INTO Messages (user_id, content, server_id) VALUES (%s, %s, %s) RETURNING message_id;",
    'select_messages': "SELECT * FROM Messages WHERE user_id = %s;",
    'select_all_messages_with_usernames': """
        SELECT Messages.content, Users.username, Messages.user_id, Users.profile_picture, Messages.message_id
        FROM Messages
        JOIN Users ON Messages.user_id = Users.user_id
        WHERE Messages.server_id = %s
        ORDER BY Messages.created_at ASC;
    """,
    'delete_message': "DELETE FROM Messages WHERE message_id = %s;",  # Mesajı sil
    'delete_messages_by_server': "DELETE FROM Messages WHERE server_id = %s;",  # Sunucuya bağlı tüm mesajları sil
    'update_message': "UPDATE Messages SET content = %s WHERE message_id = %s;",

    # Followers
    'add_follower': "INSERT INTO Followers (follower_id, followed_id) VALUES (%s, %s);",
    'remove_follower': "DELETE FROM Followers WHERE follower_id = %s AND followed_id = %s;",
    'list_followers': "SELECT follower_id FROM Followers WHERE followed_id = %s;",

    # Notifications
    'insert_notification': "INSERT INTO Notifications (user_id, content) VALUES (%s, %s);",
    'select_notifications': "SELECT * FROM Notifications WHERE user_id = %s;",
    'mark_notification_read': "UPDATE Notifications SET read = TRUE WHERE notification_id = %s;",

    # Likes
    'like_message': "INSERT INTO Likes (message_id, user_id) VALUES (%s, %s);",
    'unlike_message': "DELETE FROM Likes WHERE message_id = %s AND user_id = %s;",
    'count_likes': "SELECT COUNT(*) FROM Likes WHERE message_id = %s;"
}