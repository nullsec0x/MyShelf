from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import requests
from werkzeug.exceptions import abort
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Database initialization
def get_db_connection():
    conn = sqlite3.connect('books.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            genre TEXT NOT NULL,
            description TEXT,
            cover_url TEXT,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Auth decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
@login_required
def index():
    conn = get_db_connection()
    books = conn.execute('SELECT * FROM books WHERE user_id = ?', (session['user_id'],)).fetchall()
    conn.close()
    return render_template('index.html', books=books)

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        description = request.form.get('description', '')
        cover_url = request.form.get('cover_url', '')

        if not title or not author or not genre:
            flash('Title, author, and genre are required!', 'error')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO books (title, author, genre, description, cover_url, user_id) VALUES (?, ?, ?, ?, ?, ?)',
                         (title, author, genre, description, cover_url, session['user_id']))
            conn.commit()
            conn.close()
            flash('Book added successfully!', 'success')
            return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/details/<int:id>', methods=['GET', 'POST'])
@login_required
def book_details(id):
    conn = get_db_connection()
    book = conn.execute('SELECT * FROM books WHERE id = ? AND user_id = ?', (id, session['user_id'])).fetchone()
    conn.close()

    if book is None:
        abort(404)

    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        description = request.form.get('description', '')
        cover_url = request.form.get('cover_url', '')

        if not title or not author or not genre:
            flash('Title, author, and genre are required!', 'error')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE books SET title = ?, author = ?, genre = ?, description = ?, cover_url = ? WHERE id = ? AND user_id = ?',
                         (title, author, genre, description, cover_url, id, session['user_id']))
            conn.commit()
            conn.close()
            flash('Book updated successfully!', 'success')
            return redirect(url_for('index'))

    return render_template('details.html', book=book)

@app.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_book(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM books WHERE id = ? AND user_id = ?', (id, session['user_id']))
    conn.commit()
    conn.close()
    flash('Book deleted successfully!', 'success')
    return redirect(url_for('index'))

# Auth routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        if user is None or not check_password_hash(user['password'], password):
            flash('Invalid username or password', 'error')
        else:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))
    
    return render_template('login.html', hide_nav=True)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if not username or not password:
            flash('Username and password are required!', 'error')
        else:
            conn = get_db_connection()
            try:
                conn.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                           (username, generate_password_hash(password)))
                conn.commit()
                flash('Account created successfully! Please login.', 'success')
                return redirect(url_for('login'))
            except sqlite3.IntegrityError:
                flash('Username already exists', 'error')
            finally:
                conn.close()
    
    return render_template('signup.html', hide_nav=True)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# API route
@app.route('/search_books', methods=['GET'])
@login_required
def search_books():
    query = request.args.get('query', '')
    if not query:
        return {'error': 'No search query provided'}, 400

    try:
        response = requests.get(
            f'https://www.googleapis.com/books/v1/volumes?q={query}&maxResults=5'
        )
        data = response.json()
        
        if 'items' not in data:
            return {'results': []}
        
        results = []
        for item in data['items']:
            volume_info = item.get('volumeInfo', {})
            book = {
                'title': volume_info.get('title', ''),
                'author': ', '.join(volume_info.get('authors', ['Unknown'])),
                'genre': ', '.join(volume_info.get('categories', [''])),
                'description': volume_info.get('description', ''),
                'coverUrl': volume_info.get('imageLinks', {}).get('thumbnail', '').replace('http://', 'https://')
            }
            results.append(book)
        
        return {'results': results}
    except Exception as e:
        return {'error': str(e)}, 500

if __name__ == '__main__':
    app.run(debug=True)