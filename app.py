from flask import Flask, request, redirect, url_for, render_template, flash, session
from settings import add_user, authenticate_user, update_user, update_password, update_profile_picture, get_user_id_by_username, get_user_profile, update_user_description
from message_operations import add_message, list_all_messages_with_usernames, like_message, unlike_message, add_server, list_servers, delete_server, update_server, delete_message
from user_operations import list_users
from db_utils import execute_query
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def get_notifications(user_id):
    return execute_query('select_notifications', (user_id,), fetch_all=True)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = authenticate_user(username, password)
        if role:
            session['username'] = username
            session['role'] = role
            user_id = get_user_id_by_username(username)
            user_profile = get_user_profile(user_id)
            session['profile_picture'] = user_profile[3] if user_profile[3] else 'default.png'
            flash('Login successful!', 'success')
            return redirect(url_for('main'))
        else:
            flash('Invalid username or password. Please try again.', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form.get('role', 'user')
        description = request.form.get('description', '')
        if all([username, email, password, role]):
            if add_user(username, email, password, role, description):
                flash('Registration successful! Please login.', 'success')
                return redirect(url_for('login'))
            else:
                flash('An error occurred during registration. Please try again.', 'danger')
        else:
            flash('All fields are required. Please try again.', 'danger')
    return render_template('register.html')

@app.route('/main')
def main():
    if 'username' not in session:
        return redirect(url_for('login'))
    servers = list_servers()
    user_id = get_user_id_by_username(session['username'])
    notifications = get_notifications(user_id)
    return render_template('main.html', servers=servers, notifications=notifications)

@app.route('/server/<server_id>')
def server(server_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    messages = list_all_messages_with_usernames(server_id)
    user_id = get_user_id_by_username(session['username'])
    servers = list_servers()
    notifications = get_notifications(user_id)
    return render_template('server.html', messages=messages, user_id=user_id, server_id=server_id, servers=servers, notifications=notifications)

@app.route('/settings')
def settings():
    if 'username' not in session:
        return redirect(url_for('login'))
    user_id = get_user_id_by_username(session['username'])
    user_profile = get_user_profile(user_id)
    notifications = get_notifications(user_id)
    return render_template('settings.html', user_profile=user_profile, notifications=notifications)

@app.route('/update_user_info', methods=['POST'])
def update_user_info():
    if 'username' not in session:
        return redirect(url_for('login'))
    new_username = request.form['username']
    new_email = request.form['email']
    new_description = request.form['description']
    new_role = request.form.get('role', session['role'])  # Kullanıcının rolünü değiştirmesine izin vermeyin
    user_id = get_user_id_by_username(session['username'])
    if user_id and new_username and new_email:
        if session['role'] != 'admin':
            new_role = session['role']  # Admin olmayan kullanıcıların rolünü değiştirmesine izin vermeyin
        update_user(user_id, new_username, new_email, new_role, new_description)
        session['username'] = new_username  # Update session username
        session['role'] = new_role  # Update session role
        flash('User information updated successfully!', 'success')
    else:
        flash('All fields are required.', 'danger')
    return redirect(url_for('settings'))

@app.route('/update_password', methods=['POST'])
def update_password_route():
    if 'username' not in session:
        return redirect(url_for('login'))
    current_password = request.form['current_password']
    new_password = request.form['new_password']
    user_id = get_user_id_by_username(session['username'])
    if authenticate_user(session['username'], current_password):
        update_password(user_id, new_password)
        flash('Password updated successfully!', 'success')
    else:
        flash('Current password is incorrect.', 'danger')
    return redirect(url_for('settings'))

@app.route('/update_profile_picture', methods=['POST'])
def update_profile_picture_route():
    if 'username' not in session:
        return redirect(url_for('login'))
    user_id = get_user_id_by_username(session['username'])
    profile_picture = request.files['profile_picture']
    if profile_picture:
        profile_picture_dir = os.path.join('static', 'profile_pictures')
        if not os.path.exists(profile_picture_dir):
            os.makedirs(profile_picture_dir)
        profile_picture_filename = f"{user_id}_{profile_picture.filename}"
        profile_picture_path = os.path.join(profile_picture_dir, profile_picture_filename)
        profile_picture.save(profile_picture_path)
        update_profile_picture(user_id, profile_picture_filename)
        session['profile_picture'] = profile_picture_filename  # Update session profile picture
        flash('Profile picture updated successfully!', 'success')
    else:
        flash('Profile picture is required.', 'danger')
    return redirect(url_for('settings'))

@app.route('/profile/<username>')
def profile(username):
    if 'username' not in session:
        return redirect(url_for('login'))
    user_id = get_user_id_by_username(username)
    user_profile = get_user_profile(user_id)
    notifications = get_notifications(user_id)
    return render_template('profile.html', user_profile=user_profile, notifications=notifications)

@app.route('/message_operations', methods=['POST'])
def message_operations():
    if 'username' not in session:
        return redirect(url_for('login'))
    action = request.form['action']
    if action == 'add_message':
        content = request.form['content']
        server_id = request.form['server_id']
        user_id = get_user_id_by_username(session['username'])
        if user_id and content and server_id:
            add_message(user_id, content, server_id)
            flash('Message added successfully!', 'success')
        else:
            flash('Valid username, content, and server are required.', 'danger')
        return redirect(url_for('server', server_id=server_id))
    elif action == 'like_message':
        message_id = request.form['message_id']
        user_id = get_user_id_by_username(session['username'])
        if message_id and user_id:
            like_message(message_id, user_id)
            flash('Message liked successfully!', 'success')
        else:
            flash('Message ID and valid username are required.', 'danger')
    elif action == 'unlike_message':
        message_id = request.form['message_id']
        user_id = get_user_id_by_username(session['username'])
        if message_id and user_id:
            unlike_message(message_id, user_id)
            flash('Message unliked successfully!', 'success')
        else:
            flash('Message ID and valid username are required.', 'danger')
    return redirect(url_for('server', server_id=request.form.get('server_id', '')))

@app.route('/add_server', methods=['POST'])
def add_server_route():
    server_name = request.form['server_name']
    if server_name:
        add_server(server_name)
        flash('Server added successfully!', 'success')
    else:
        flash('Server name is required.', 'danger')
    return redirect(url_for('main'))

@app.route('/delete_server', methods=['POST'])
def delete_server_route():
    if 'username' not in session or session.get('role') != 'admin':
        flash('You do not have permission to perform this action.', 'danger')
        return redirect(url_for('main'))
    server_id = request.form['server_id']
    print(f"Deleting server with ID: {server_id}")  # Hata ayıklama için log ekleyin
    result = delete_server(server_id)
    print(f"Delete result: {result}")  # Hata ayıklama için log ekleyin
    flash('Server deleted successfully!', 'success')
    return redirect(url_for('main'))

@app.route('/update_server', methods=['POST'])
def update_server_route():
    if 'username' not in session or session.get('role') != 'admin':
        flash('You do not have permission to perform this action.', 'danger')
        return redirect(url_for('main'))
    server_id = request.form['server_id']
    server_name = request.form['server_name']
    update_server(server_id, server_name)
    flash('Server updated successfully!', 'success')
    return redirect(url_for('main'))

@app.route('/delete_message', methods=['POST'])
def delete_message_route():
    if 'username' not in session or session.get('role') != 'admin':
        flash('You do not have permission to perform this action.', 'danger')
        return redirect(url_for('main'))
    message_id = request.form['message_id']
    server_id = request.form['server_id']
    print(f"Deleting message with ID: {message_id}")  # Hata ayıklama için log ekleyin
    result = delete_message(message_id)
    print(f"Delete result: {result}")  # Hata ayıklama için log ekleyin
    if result is None:
        flash('Failed to delete message.', 'danger')
    else:
        flash('Message deleted successfully!', 'success')
    return redirect(url_for('server', server_id=server_id))

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('profile_picture', None)
    session.pop('role', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/search')
def search():
    query = request.args.get('query')
    user_id = get_user_id_by_username(query)
    if user_id:
        return redirect(url_for('profile', username=query))
    else:
        flash(f'User {query} not found.', 'danger')
        return redirect(url_for('main'))

@app.route('/admin')
def admin():
    if 'username' not in session or session.get('role') != 'admin':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('main'))
    users = list_users()
    user_id = get_user_id_by_username(session['username'])
    notifications = get_notifications(user_id)
    return render_template('admin.html', users=users, notifications=notifications)

@app.route('/update_user_role', methods=['POST'])
def update_user_role():
    if 'username' not in session or session.get('role') != 'admin':
        flash('You do not have permission to perform this action.', 'danger')
        return redirect(url_for('main'))
    
    user_id = request.form['user_id']
    new_role = request.form['role']
    
    # Hedef kullanıcının mevcut rolünü al
    target_user_profile = get_user_profile(user_id)
    target_user_role = target_user_profile[4]  # Rol bilgisi 5. sütunda
    
    # Eğer hedef kullanıcı admin ise, rol değişikliğine izin verme
    if target_user_role == 'admin':
        flash('You cannot change the role of another admin.', 'danger')
        return redirect(url_for('admin'))
    
    update_user(user_id, role=new_role)
    
    # Eğer güncellenen kullanıcı oturum açmış kullanıcı ise, oturumdaki rol bilgisini güncelle
    if user_id == get_user_id_by_username(session['username']):
        session['role'] = new_role
    
    flash('User role updated successfully!', 'success')
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)