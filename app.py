from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import sqlite3
app = Flask(__name__)
app.secret_key = "a"

def get_db_connection():
    conn = sqlite3.connect('flask_login.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    db = get_db_connection()
    with app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
    db.commit()
    db.close()
    print('Initialized database.')
    if not os.path.exists('flask_login.db'):
        init_db()
        print('Database created and initialized.')
    else:
        print('Database already exists, skipping initialization.')
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/quiz', methods=['GET', 'POST'])

def quiz():
    '''
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        answers = request.form
        score = 0
        correct_answers = {'q1': 'a', 'q2': 'b', 'q3': 'c'}
        for key, value in correct_answers.items():
            if answers.get(key) == value:
                score += 1
        return redirect(url_for('index'))
    return render_template('quiz.html')
'''
    return render_template('quiz.html')
@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute('INSERT INTO users (username, password, email) VALUES (?, ?, ?)', (username, password, email))
        db.commit()
        db.close()
        flash('You have successfully registered.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle user login. On GET request, it renders the login page.
    On POST request, it validates the credentials and logs the user in.
    """
    if request.method == 'POST':
        # Retrieve the user-provided email and password from the form
        email = request.form.get('email')
        password = request.form.get('password')

        # Validate that the email and password fields are not empty
        if not email or not password:
            flash('Email and password are required.', 'error')
            return render_template('login.html')

        # Connect to the database to retrieve user information
        db = get_db_connection()
        cursor = db.cursor()

        # Fetch user details by email
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        db.close()  # Always close the database connection after query

        if user is None:
            # If no user is found with the provided email address
            flash('Invalid email or password.', 'error')
            return render_template('login.html')

        # Compare the provided password directly with the stored password
        stored_password = user['password']  # Assuming passwords are stored in plain text
        if password == stored_password:
            # If passwords match, log the user in by storing their session
            session['username'] = user['username']  # Store the username in the session
            flash('Login successful!', 'success')
            return redirect(url_for('index'))  # Redirect to the homepage or dashboard
        else:
            # If the password is incorrect
            flash('Invalid email or password.', 'error')
            return render_template('login.html')

    # If it's a GET request, simply render the login page
    return render_template('login.html')

if __name__ == '__main__':
    init_db()
    app.run(port=5001, debug=True)