-- Roles Tablosu
CREATE TABLE Roles (
    role_id SERIAL PRIMARY KEY,
    role_name VARCHAR(50) NOT NULL UNIQUE
);

-- Varsayılan roller ekle
INSERT INTO Roles (role_name) VALUES ('admin'), ('user');

-- Users Tablosu
CREATE TABLE Users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    description TEXT,
    profile_picture VARCHAR(255),
    role_id INT,
    FOREIGN KEY (role_id) REFERENCES Roles(role_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Servers Tablosu
CREATE TABLE Servers (
    server_id SERIAL PRIMARY KEY,
    server_name VARCHAR(100) NOT NULL
);

-- Messages Tablosu
CREATE TABLE Messages (
    message_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    content TEXT NOT NULL,
    server_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (server_id) REFERENCES Servers(server_id) ON DELETE CASCADE
);

-- Followers Tablosu
CREATE TABLE Followers (
    follower_id INT NOT NULL,
    followed_id INT NOT NULL,
    PRIMARY KEY (follower_id, followed_id),
    FOREIGN KEY (follower_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (followed_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- Notifications Tablosu
CREATE TABLE Notifications (
    notification_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    content TEXT NOT NULL,
    sender_id INT NOT NULL,
    read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (sender_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- Likes Tablosu
CREATE TABLE Likes (
    message_id INT NOT NULL,
    user_id INT NOT NULL,
    PRIMARY KEY (message_id, user_id),
    FOREIGN KEY (message_id) REFERENCES Messages(message_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- BlockedUsers Tablosu
CREATE TABLE BlockedUsers (
    blocker_id INT NOT NULL,
    blocked_id INT NOT NULL,
    PRIMARY KEY (blocker_id, blocked_id),
    FOREIGN KEY (blocker_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (blocked_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- Comments Tablosu
CREATE TABLE Comments (
    comment_id SERIAL PRIMARY KEY,
    message_id INT NOT NULL,
    user_id INT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (message_id) REFERENCES Messages(message_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- DirectMessages Tablosu
CREATE TABLE DirectMessages (
    dm_id SERIAL PRIMARY KEY,
    sender_id INT NOT NULL,
    receiver_id INT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (receiver_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- Media Tablosu
CREATE TABLE Media (
    media_id SERIAL PRIMARY KEY,
    message_id INT,
    user_id INT NOT NULL,
    media_url VARCHAR(255) NOT NULL,
    media_type VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (message_id) REFERENCES Messages(message_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- Reports Tablosu
CREATE TABLE Reports (
    report_id SERIAL PRIMARY KEY,
    reported_by INT NOT NULL,
    reported_user INT,
    reported_message INT,
    report_reason TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (reported_by) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (reported_user) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (reported_message) REFERENCES Messages(message_id) ON DELETE CASCADE
);

-- SavedMessages Tablosu
CREATE TABLE SavedMessages (
    user_id INT NOT NULL,
    message_id INT NOT NULL,
    PRIMARY KEY (user_id, message_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (message_id) REFERENCES Messages(message_id) ON DELETE CASCADE
);

-- Tetikleyici Fonksiyonu: Yeni Mesaj Eklendiğinde Bildirim Ekleme
CREATE OR REPLACE FUNCTION notify_new_message()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO Notifications (user_id, content, sender_id)
    VALUES (NEW.user_id, 'New message added: ' || NEW.content, NEW.user_id);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Tetikleyici: Yeni Mesaj Eklendiğinde Bildirim Ekleme
CREATE TRIGGER after_message_insert
AFTER INSERT ON Messages
FOR EACH ROW
EXECUTE FUNCTION notify_new_message();

-- Tetikleyici Fonksiyonu: Yeni DM Eklendiğinde Bildirim Ekleme
CREATE OR REPLACE FUNCTION notify_new_dm()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO Notifications (user_id, content, sender_id)
    VALUES (NEW.receiver_id, (SELECT username FROM Users WHERE user_id = NEW.sender_id) || ' tarafından bir mesaj var', NEW.sender_id);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Tetikleyici: Yeni DM Eklendiğinde Bildirim Ekleme
CREATE TRIGGER after_dm_insert
AFTER INSERT ON DirectMessages
FOR EACH ROW
EXECUTE FUNCTION notify_new_dm();

-- Tetikleyici Fonksiyonu: Kullanıcı Silindiğinde İlişkili Verileri Silme
CREATE OR REPLACE FUNCTION delete_user_related_data()
RETURNS TRIGGER AS $$
BEGIN
    DELETE FROM Messages WHERE user_id = OLD.user_id;
    DELETE FROM Followers WHERE follower_id = OLD.user_id OR followed_id = OLD.user_id;
    DELETE FROM Notifications WHERE user_id = OLD.user_id;
    DELETE FROM Likes WHERE user_id = OLD.user_id;
    DELETE FROM BlockedUsers WHERE blocker_id = OLD.user_id OR blocked_id = OLD.user_id;
    DELETE FROM Comments WHERE user_id = OLD.user_id;
    DELETE FROM DirectMessages WHERE sender_id = OLD.user_id OR receiver_id = OLD.user_id;
    DELETE FROM Media WHERE user_id = OLD.user_id;
    DELETE FROM Reports WHERE reported_by = OLD.user_id OR reported_user = OLD.user_id;
    DELETE FROM SavedMessages WHERE user_id = OLD.user_id;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

-- Tetikleyici: Kullanıcı Silindiğinde İlişkili Verileri Silme
CREATE TRIGGER after_user_delete
AFTER DELETE ON Users
FOR EACH ROW
EXECUTE FUNCTION delete_user_related_data();

CREATE TABLE admins (
    admin_id SERIAL PRIMARY KEY,
    permission_level INT NOT NULL
) INHERITS (users);