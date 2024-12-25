# sql_queries.py
QUERIES = {
    # Users
    'insert_user': "INSERT INTO Users (username, email, password, role_id, description) VALUES (%s, %s, %s, %s, %s) RETURNING user_id;",
    'select_users': """
        SELECT Users.user_id, Users.username, Users.email, Users.password, Users.description, Users.profile_picture, Roles.role_name
        FROM Users
        JOIN Roles ON Users.role_id = Roles.role_id;
    """,
    'delete_user': "DELETE FROM Users WHERE user_id = %s;",
    'update_user': "UPDATE Users SET username = %s, email = %s, role_id = %s, description = %s WHERE user_id = %s;",
    'update_user_role': "UPDATE Users SET role_id = %s WHERE user_id = %s;",
    'authenticate_user': """
        SELECT Users.password, Roles.role_name
        FROM Users
        JOIN Roles ON Users.role_id = Roles.role_id
        WHERE Users.username = %s;
    """,
    'get_user_id_by_username': "SELECT user_id FROM Users WHERE username = %s;",
    'select_user_profile': """
        SELECT Users.user_id, Users.username, Users.email, Users.profile_picture, Roles.role_name, Users.description
        FROM Users
        JOIN Roles ON Users.role_id = Roles.role_id
        WHERE Users.user_id = %s;
    """,
    'update_profile_picture': "UPDATE Users SET profile_picture = %s WHERE user_id = %s;",
    'update_user_description': "UPDATE Users SET description = %s WHERE user_id = %s;",
    'get_role_id_by_name': "SELECT role_id FROM Roles WHERE role_name = %s;",

    # Servers
    'insert_server': "INSERT INTO Servers (server_name) VALUES (%s) RETURNING server_id;",
    'select_servers': "SELECT * FROM Servers;",
    'delete_server': "DELETE FROM Servers WHERE server_id = %s;",
    'update_server': "UPDATE Servers SET server_name = %s WHERE server_id = %s;",

    # Messages
    'insert_message': "INSERT INTO Messages (user_id, content, server_id) VALUES (%s, %s, %s) RETURNING message_id;",
    'select_messages': "SELECT * FROM Messages WHERE user_id = %s;",
    'select_all_messages_with_usernames': """
        SELECT Messages.content, Users.username, Messages.user_id, Users.profile_picture, Messages.message_id, Messages.created_at
        FROM Messages
        JOIN Users ON Messages.user_id = Users.user_id
        WHERE Messages.server_id = %s
        ORDER BY Messages.created_at ASC;  -- Mesajları gönderim tarihine göre sıralar
    """,
    'delete_message': "DELETE FROM Messages WHERE message_id = %s;",
    'delete_messages_by_server': "DELETE FROM Messages WHERE server_id = %s;",
    'update_message': "UPDATE Messages SET content = %s WHERE message_id = %s;",
    'get_message_author': "SELECT user_id FROM Messages WHERE message_id = %s;",  # Yeni sorgu eklendi

    # Followers
    'add_follower': "INSERT INTO Followers (follower_id, followed_id) VALUES (%s, %s);",
    'remove_follower': "DELETE FROM Followers WHERE follower_id = %s AND followed_id = %s;",
    'count_followers': "SELECT COUNT(*) FROM Followers WHERE followed_id = %s;",

    # Notifications
    'insert_notification': "INSERT INTO Notifications (user_id, content, sender_id) VALUES (%s, %s, %s);",
    'select_notifications': "SELECT * FROM Notifications WHERE user_id = %s;",
    'select_notification_by_id': "SELECT * FROM Notifications WHERE notification_id = %s;",
    'mark_notification_read': "UPDATE Notifications SET read = TRUE WHERE notification_id = %s;",

    # Likes
    'like_message': "INSERT INTO Likes (message_id, user_id) VALUES (%s, %s);",
    'unlike_message': "DELETE FROM Likes WHERE message_id = %s AND user_id = %s;",
    'count_likes': "SELECT COUNT(*) FROM Likes WHERE message_id = %s;",

    # Direct Messages
    'insert_dm': "INSERT INTO DirectMessages (sender_id, receiver_id, content) VALUES (%s, %s, %s) RETURNING dm_id;",
    'select_dms': """
        SELECT DirectMessages.content, Users.username, DirectMessages.sender_id, Users.profile_picture, DirectMessages.dm_id, DirectMessages.created_at
        FROM DirectMessages
        JOIN Users ON DirectMessages.sender_id = Users.user_id
        WHERE (DirectMessages.receiver_id = %s AND DirectMessages.sender_id = %s)
           OR (DirectMessages.receiver_id = %s AND DirectMessages.sender_id = %s)
        ORDER BY DirectMessages.created_at ASC;  -- Mesajları gönderim tarihine göre sıralar
    """,
    
    'list_dm_conversations': """
        SELECT DISTINCT ON (Users.user_id) Users.user_id, Users.username
        FROM DirectMessages
        JOIN Users ON DirectMessages.sender_id = Users.user_id OR DirectMessages.receiver_id = Users.user_id
        WHERE (DirectMessages.sender_id = %s OR DirectMessages.receiver_id = %s) AND Users.user_id != %s;
    """,
    'delete_dm': "DELETE FROM DirectMessages WHERE dm_id = %s;",

    # Blocked Users
    'block_user': "INSERT INTO BlockedUsers (blocker_id, blocked_id) VALUES (%s, %s);",
    'unblock_user': "DELETE FROM BlockedUsers WHERE blocker_id = %s AND blocked_id = %s;",
    'is_user_blocked': "SELECT 1 FROM BlockedUsers WHERE blocker_id = %s AND blocked_id = %s;",
}