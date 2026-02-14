from flask import Flask, render_template, request, redirect, session, url_for, send_from_directory
import os
import json
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'RITU_SECURE_KEY_2026'  # Required for login security

# --- CONFIGURATION ---
UPLOAD_FOLDER = 'uploads'
DB_FILE = 'database.json'

# Auto-create necessary folders
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# --- DATABASE SYSTEM ---
def load_db():
    if not os.path.exists(DB_FILE):
        # Create a default welcome post if DB is empty
        default_data = [{
            "id": 1,
            "type": "image",
            "title": "Welcome to my Portfolio",
            "date": "2026",
            "desc": "This is the start of my digital journey.",
            "filename": "default_placeholder.jpg" 
        }]
        with open(DB_FILE, 'w') as f:
            json.dump(default_data, f)
        return default_data
    
    with open(DB_FILE, 'r') as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# --- ROUTES ---
@app.route('/')
def home():
    posts = load_db()
    return render_template('index.html', posts=posts)

@app.route('/login', methods=['POST'])
def login():
    # YOUR ADMIN CREDENTIALS
    if request.form['email'] == 'rritu8786@gmail.com' and request.form['password'] == 'Ritu@100504':
        session['logged_in'] = True
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('home'))

@app.route('/add', methods=['POST'])
def add_post():
    if 'logged_in' not in session: return redirect(url_for('home'))
    
    file = request.files['file']
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        posts = load_db()
        new_post = {
            "id": len(posts) + 100,
            "type": request.form['type'],
            "title": request.form['title'],
            "date": request.form['date'],
            "desc": request.form['desc'],
            "filename": filename
        }
        posts.insert(0, new_post) # Add new post to the top
        save_db(posts)
        
    return redirect(url_for('home'))

@app.route('/delete', methods=['POST'])
def delete_post():
    if 'logged_in' not in session: return redirect(url_for('home'))
    
    post_id = int(request.form['id'])
    posts = load_db()
    # Filter out the post to be deleted
    posts = [p for p in posts if p['id'] != post_id]
    save_db(posts)
    
    return redirect(url_for('home'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)