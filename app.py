# app.py
from flask import Flask, request, redirect, url_for, render_template, flash, session
from user_operations import add_user, list_users, delete_user, update_user, authenticate_user, get_user_id_by_username
from message_operations import add_message, list_messages, list_all_messages_with_usernames, delete_message, update_message, like_message, unlike_message, count_likes

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def home():
    messages = list_all_messages_with_usernames()
    return render_template('home.html', messages=messages)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if authenticate_user(username, password):
            session['username'] = username
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
    return render_template('main.html')

@app.route('/user_operations')
def user_operations():
    if 'username' not in session:
        return redirect(url_for('login'))
    users = list_users()
    return render_template('user_operations.html', users=users)

@app.route('/message_operations', methods=['GET', 'POST'])
def message_operations():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        action = request.form['action']
        if action == 'add_message':
            content = request.form['content']
            user_id = get_user_id_by_username(session['username'])
            if user_id and content:
                add_message(user_id, content)
                flash('Message added successfully!', 'success')
            else:
                flash('Valid username and content are required.', 'danger')
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
    messages = list_messages(get_user_id_by_username(session['username']))
    return render_template('message_operations.html', messages=messages)

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)