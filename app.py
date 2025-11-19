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

@app.route('/expedition')
def expedition():
    return render_template('expedition.html')

@app.route('/sever')
def sever():
    return render_template('sever.html')
@app.route('/firewatch')
def firewatch():
    return render_template('firewatch.html')
@app.route('/edithfinch')
def edithfinch():
    return render_template('edithfinch.html')
@app.route('/beforeyoureyes')
def beforeyoureyes():
    return render_template('beforeyoureyes.html')
@app.route('/omori')
def omori():
    return render_template('omori.html')
@app.route('/expeditionreco')
def expeditionreco():
    return render_template('expeditionreco.html')

@app.route('/severreco')
def severreco():
    return render_template('severreco.html')
@app.route('/firewatchreco')
def firewatchreco():
    return render_template('firewatchreco.html')
@app.route('/edithfinchreco')
def edithfincreco():
    return render_template('edithfinchreco.html')
@app.route('/beforeyoureyesreco')
def beforeyoureyesreco():
    return render_template('beforeyoureyesreco.html')
@app.route('/omorireco')
def omorireco():
    return render_template('omorireco.html')
@app.route('/games')
def games():
   return render_template('games.html')
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
@app.route('/playlist')
def playlist():
    if 'username' not in session:
        flash('Please log in to view your playlist.', 'error')
        return redirect(url_for('login'))

    db = get_db_connection()
    cursor = db.cursor()

    # Get the current user ID
    cursor.execute('SELECT id FROM users WHERE username = ?', (session['username'],))
    user = cursor.fetchone()
    if not user:
        db.close()
        flash('User not found.', 'error')
        return redirect(url_for('index'))

    user_id = user['id']

    # Fetch games from playlist
    cursor.execute('SELECT * FROM playlist WHERE user_id = ?', (user_id,))
    games = cursor.fetchall()
    db.close()

    return render_template('playlist.html', games=games)


@app.route('/_playlist/<game_id>', methods=['POST'])
def add_to_playlist(game_id):
    if 'username' not in session:
        flash('Please log in to add games to your playlist.', 'error')
        return redirect(url_for('login'))

    #game database
    game_db = {
        'beforeyoureyes': {
            'name': 'Before Your Eyes',
            'img': 'https://i.ytimg.com/vi/hN2aqi5MhXo/maxresdefault.jpg',
            'link': 'https://www.beforeyoureyesgame.com/#about'
        },
        'sever': {
            'name': 'Sever',
            'img': 'https://tr.rbxcdn.com/180DAY-733439886b2d74c27ea4f13e2e490640/768/432/Image/Webp/noFilter',
            'link': 'https://www.roblox.com/games/80643569017414/Sever'
        },
        'expedition': {
            'name': 'Expedition',
            'img': 'https://tr.rbxcdn.com/180DAY-bf16625d0900c55a5242eaa06c4e6d6e/768/432/Image/Webp/noFilter',
            'link': 'https://www.roblox.com/games/14396787128/EXPEDITION'
        },
        'firewatch': {
            'name': 'Firewatch',
            'img': 'https://tse2.mm.bing.net/th/id/OIP.kpGJcQ6g7rjGZStdmTPz8AHaEK?rs=1&pid=ImgDetMain&o=7&rm=3',
            'link': 'https://www.firewatchgame.com/'
        },
        'edithfinch': {
            'name': 'What Remains of Edith Finch',
            'img': 'https://tse2.mm.bing.net/th/id/OIP.tVSU5Znmq1w8wGrWp0Po8QHaEK?rs=1&pid=ImgDetMain&o=7&rm=3',
            'link': 'https://www.annapurna.com/interactive/what-remains-of-edith-finch'
        },
        'omori': {
            'name': 'Omori',
            'img': 'https://artfiles.alphacoders.com/140/140072.jpg',
            'link': 'https://omori-game.com/en'
        }
    }

    game = game_db.get(game_id)
    if not game:
        flash('Game not found.', 'error')
        return redirect(url_for('playlist'))

    db = get_db_connection()
    cursor = db.cursor()

    # Get user ID
    cursor.execute('SELECT id FROM users WHERE username = ?', (session['username'],))
    user = cursor.fetchone()
    if not user:
        db.close()
        flash('User not found.', 'error')
        return redirect(url_for('playlist'))

    user_id = user['id']

    # Check if game already in playlist
    cursor.execute('SELECT * FROM playlist WHERE user_id = ? AND game_id = ?', (user_id, game_id))
    existing = cursor.fetchone()

    if existing:
        flash(f"{game['name']} is already in your play list.", 'info')
    else:
        cursor.execute(
            'INSERT INTO playlist (user_id, game_id, game_name, game_img, game_link) VALUES (?, ?, ?, ?, ?)',
            (user_id, game_id, game['name'], game['img'], game['link'])
        )
        db.commit()
        flash(f"Added {game['name']} to your play list!", 'success')

    db.close()
    return redirect(url_for('playlist'))


@app.route('/remove_from_playlist/<game_id>', methods=['POST'])
def remove_from_playlist(game_id):
    if 'username' not in session:
        flash('Please log in to modify your playlist.', 'error')
        return redirect(url_for('login'))

    db = get_db_connection()
    cursor = db.cursor()

    # Get user ID
    cursor.execute('SELECT id FROM users WHERE username = ?', (session['username'],))
    user = cursor.fetchone()
    if not user:
        db.close()
        flash('User not found.', 'error')
        return redirect(url_for('playlist'))

    user_id = user['id']

    # Delete the selected game for that user
    cursor.execute('DELETE FROM playlist WHERE user_id = ? AND game_id = ?', (user_id, game_id))
    db.commit()
    db.close()

    flash('Game removed from your play list.', 'info')
    return redirect(url_for('playlist'))



if __name__ == '__main__':
    init_db()
    app.run(port=5003, debug=True)