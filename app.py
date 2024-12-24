# app.py
from flask import Flask, request, redirect, url_for, render_template, flash, session
from settings import add_user, authenticate_user, update_user, update_password, update_profile_picture, get_user_id_by_username, get_user_profile
from message_operations import add_message, list_all_messages_with_usernames, like_message, unlike_message, add_server, list_servers
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if authenticate_user(username, password):
            session['username'] = username
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
        if username and email and password:
            add_user(username, email, password)
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        else:
            flash('All fields are required. Please try again.', 'danger')
    return render_template('register.html')

@app.route('/main')
def main():
    if 'username' not in session:
        return redirect(url_for('login'))
    servers = list_servers()
    return render_template('main.html', servers=servers)

@app.route('/server/<server_id>')
def server(server_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    messages = list_all_messages_with_usernames(server_id)
    user_id = get_user_id_by_username(session['username'])
    servers = list_servers()
    return render_template('server.html', messages=messages, user_id=user_id, server_id=server_id, servers=servers)

@app.route('/settings')
def settings():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('settings.html')

@app.route('/update_user_info', methods=['POST'])
def update_user_info():
    if 'username' not in session:
        return redirect(url_for('login'))
    new_username = request.form['username']
    new_email = request.form['email']
    user_id = get_user_id_by_username(session['username'])
    if user_id and new_username and new_email:
        update_user(user_id, new_username, new_email)
        session['username'] = new_username  # Update session username
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
    return render_template('profile.html', user_profile=user_profile)

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

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('profile_picture', None)
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

if __name__ == '__main__':
    app.run(debug=True)