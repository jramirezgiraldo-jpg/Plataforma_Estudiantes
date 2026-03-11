import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
import os
import glob

app = Flask(__name__)
app.secret_key = 'super_secret_key_educativa_2026'

# Carpeta donde están los documentos HTML del profesor (Adaptado para producción)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GUIAS_PATH = os.path.join(BASE_DIR, "Guias_1p")

def get_db_connection():
    db_path = os.path.join(BASE_DIR, 'users.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            name TEXT NOT NULL,
            grade INTEGER NOT NULL,
            score REAL DEFAULT 0.0,
            completed INTEGER DEFAULT 0,
            is_admin BOOLEAN DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def get_animal_reward(score):
    if score >= 4.5:
        return 'eagle'
    elif score >= 3.5:
        return 'tiger'
    elif score >= 2.5:
        return 'fox'
    elif score >= 1.5:
        return 'owl'
    return 'tortoise'

# Categorizar los archivos por grado
def get_files_for_grade(grade):
    # grade podría ser un entero 6, 7, 8, 9, 10, 11
    # Los archivos empiezan con "6 ", "7 ", "10 ", etc.
    # Listamos todos los html de Guias 1p
    if not os.path.exists(GUIAS_PATH):
        return []
    
    files = []
    # Buscamos archivos que comiencen por "{grade} " o "{grade}_"
    # Tambien hay excepciones como "6-11 mapas .html" que aplican a todos.
    
    all_files = os.listdir(GUIAS_PATH)
    for f in all_files:
        if f.endswith('.html') or f.endswith('.py'):
            # Si el archivo empieza por "6 " y el grado es 6
            if f.startswith(f"{grade} ") or f.startswith(f"{grade}_") or f.startswith(f"{grade}-"):
                # Formatear el nombre para mostrarlo bonito
                display_name = f.replace('.html', '').replace('.py', '')
                files.append({'filename': f, 'display_name': display_name})
    
    # Ordenar alfabéticamente
    files.sort(key=lambda x: x['display_name'])
    return files

@app.route('/')
def index():
    if 'user_id' in session:
        if session.get('is_admin'):
            return redirect(url_for('admin_dashboard'))
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        name = request.form['name'].strip()
        grade = int(request.form['grade'])
        
        if not username or not password or not name or not grade:
            flash('Por favor llena todos los campos', 'error')
        else:
            db = get_db_connection()
            try:
                db.execute(
                    'INSERT INTO users (username, password, name, grade) VALUES (?, ?, ?, ?)',
                    (username, generate_password_hash(password), name, grade)
                )
                db.commit()
                flash('Registro exitoso. ¡Ahora puedes iniciar sesión!', 'success')
                return redirect(url_for('login'))
            except sqlite3.IntegrityError:
                flash(f'El usuario {username} ya está registrado.', 'error')
            finally:
                db.close()
                
    return render_template('register.html')

@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        
        db = get_db_connection()
        user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        db.close()
        
        if user is None:
            flash('Usuario incorrecto.', 'error')
        elif not check_password_hash(user['password'], password):
            flash('Contraseña incorrecta.', 'error')
        else:
            session.clear()
            session['user_id'] = user['id']
            session['name'] = user['name']
            session['grade'] = user['grade']
            session['is_admin'] = user['is_admin']
            
            if user['is_admin']:
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('dashboard'))
            
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session or session.get('is_admin'):
        return redirect(url_for('login'))
        
    grade = session['grade']
    name = session['name']
    files = get_files_for_grade(grade)
    
    db = get_db_connection()
    user = db.execute('SELECT score, completed FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    db.close()
    
    score = user['score'] if user else 0.0
    completed = user['completed'] if user else 0
    animal = get_animal_reward(score)
    
    return render_template('dashboard.html', files=files, name=name, grade=grade, score=score, completed=completed, animal=animal)

@app.route('/complete_activity', methods=['POST'])
def complete_activity():
    if 'user_id' not in session or session.get('is_admin'):
        return {'status': 'error'}, 403
    
    db = get_db_connection()
    user = db.execute('SELECT score, completed FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    
    if user:
        new_completed = user['completed'] + 1
        new_score = min(5.0, user['score'] + 0.5)
        db.execute('UPDATE users SET score = ?, completed = ? WHERE id = ?', (new_score, new_completed, session['user_id']))
        db.commit()
    db.close()
    
    return {'status': 'success'}

@app.route('/admin_dashboard')
def admin_dashboard():
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('login'))
        
    grade_filter = request.args.get('grade', type=int)
    
    db = get_db_connection()
    if grade_filter:
        students = db.execute('SELECT * FROM users WHERE is_admin = 0 AND grade = ? ORDER BY score DESC, completed DESC', (grade_filter,)).fetchall()
    else:
        students = db.execute('SELECT * FROM users WHERE is_admin = 0 ORDER BY score DESC, completed DESC').fetchall()
    db.close()
    
    student_data = []
    for s in students:
        student_data.append({
            'name': s['name'],
            'grade': s['grade'],
            'score': s['score'],
            'completed': s['completed'],
            'animal': get_animal_reward(s['score'])
        })
        
    return render_template('admin_dashboard.html', students=student_data, name=session['name'], selected_grade=grade_filter)

@app.route('/material/<filename>')
def serve_material(filename):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Simple seguridad para evitar salir del directorio
    # En producción habría que ser más riguroso
    if '/' in filename or '\\' in filename:
        return "Acceso denegado", 403
        
    return send_from_directory(GUIAS_PATH, filename)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=3000)
