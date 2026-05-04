import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
import os
import glob
from urllib.parse import urlparse

from translations import TRANSLATIONS

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'super_secret_key_educativa_2026')

# --- INTERNACIONALIZACIÓN (i18n) ---
@app.context_processor
def inject_translate():
    def t(key):
        lang = session.get('lang', 'es')
        return TRANSLATIONS.get(lang, TRANSLATIONS['es']).get(key, key)
    return dict(t=t)

@app.route('/set_language/<lang>')
def set_language(lang):
    if lang in TRANSLATIONS:
        session['lang'] = lang
    return redirect(request.referrer or url_for('index'))

# Configuración de Rutas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GUIAS_1P_PATH = os.path.join(BASE_DIR, "Guias_1p")
GUIAS_2P_PATH = os.path.join(BASE_DIR, "Guias_2p")

# --- LÓGICA DE PERSISTENCIA DE DATOS (SQLite / PostgreSQL) ---
def get_db_connection():
    db_url = os.environ.get('DATABASE_URL')
    if db_url:
        conn = psycopg2.connect(db_url, sslmode='require')
        conn.cursor_factory = RealDictCursor
        return conn
    else:
        db_path = os.path.join(BASE_DIR, 'users.db')
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn

def execute_query(query, params=(), fetchone=False, fetchall=False, commit=False):
    conn = get_db_connection()
    is_postgres = os.environ.get('DATABASE_URL') is not None
    if is_postgres:
        query = query.replace('?', '%s')
    
    try:
        cur = conn.cursor()
        cur.execute(query, params)
        result = None
        if fetchone: result = cur.fetchone()
        elif fetchall: result = cur.fetchall()
        if commit: conn.commit()
        return result
    finally:
        conn.close()

def init_db():
    is_postgres = os.environ.get('DATABASE_URL') is not None
    
    # Tabla de Usuarios Evolucionada
    users_query = '''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY, 
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            name TEXT NOT NULL,
            grade INTEGER NOT NULL,
            score REAL DEFAULT 0.0,
            completed INTEGER DEFAULT 0,
            role TEXT DEFAULT 'student'
        )
    '''
    
    # Tabla de Actividades para Padres (SaaS Focus)
    activities_query = '''
        CREATE TABLE IF NOT EXISTS parent_activities (
            id SERIAL PRIMARY KEY,
            parent_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            normative TEXT,
            grade INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    '''

    if not is_postgres:
        users_query = users_query.replace('SERIAL PRIMARY KEY', 'INTEGER PRIMARY KEY AUTOINCREMENT')
        activities_query = activities_query.replace('SERIAL PRIMARY KEY', 'INTEGER PRIMARY KEY AUTOINCREMENT')
        activities_query = activities_query.replace('DEFAULT CURRENT_TIMESTAMP', "DEFAULT (datetime('now','localtime'))")

    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute(users_query)
        cur.execute(activities_query)
        
        # Admin Default (Teacher Portal)
        cur.execute("SELECT COUNT(*) as count FROM users WHERE role = 'teacher'")
        if is_postgres:
            count = cur.fetchone()['count']
        else:
            count = cur.fetchone()['count']
            
        if count == 0:
            cur.execute(
                "INSERT INTO users (username, password, name, grade, role) VALUES (?, ?, ?, ?, ?)",
                ("9770462", generate_password_hash("Biol2008%"), "Admin Juan Felipe", 11, "teacher")
            ) if not is_postgres else cur.execute(
                "INSERT INTO users (username, password, name, grade, role) VALUES (%s, %s, %s, %s, %s)",
                ("9770462", generate_password_hash("Biol2008%"), "Admin Juan Felipe", 11, "teacher")
            )
            
        conn.commit()
    except Exception as e:
        print(f"Error initializing DB: {e}")
    finally:
        conn.close()

# --- HELPERS ---
def get_animal_reward(score):
    if score >= 4.5: return 'eagle'
    elif score >= 3.5: return 'tiger'
    elif score >= 2.5: return 'fox'
    elif score >= 1.5: return 'owl'
    return 'tortoise'

def get_files_for_grade(grade):
    files = []
    for periodo, path in [('1P', GUIAS_1P_PATH), ('2P', GUIAS_2P_PATH)]:
        if os.path.exists(path):
            all_files = os.listdir(path)
            for f in all_files:
                if f.endswith('.html') or f.endswith('.py'):
                    if f.startswith(f"{grade} ") or f.startswith(f"{grade}_") or f.startswith(f"{grade}-"):
                        display_name = f.replace('.html', '').replace('.py', '')
                        files.append({'filename': f, 'display_name': display_name, 'periodo': periodo, 'type': 'official'})
    
    # Cargar actividades creadas por padres para este grado
    p_activities = execute_query('SELECT * FROM parent_activities WHERE grade = ?', (grade,), fetchall=True)
    for pa in p_activities:
        files.append({
            'filename': '#', 
            'display_name': pa['title'], 
            'periodo': 'Homeschooling', 
            'type': 'parental',
            'desc': pa['description'],
            'norm': pa['normative']
        })
        
    files.sort(key=lambda x: (x['periodo'], x['display_name']))
    return files

# --- RUTAS ---
@app.route('/')
def index():
    if 'user_id' in session:
        role = session.get('role')
        if role == 'teacher': return redirect(url_for('admin_dashboard'))
        elif role == 'parent': return redirect(url_for('parent_dashboard'))
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login_docente', methods=('GET', 'POST'))
def login_docente():
    return portal_login('teacher')

@app.route('/login_estudiante', methods=('GET', 'POST'))
def login_estudiante():
    return portal_login('student')

@app.route('/login_padres', methods=('GET', 'POST'))
def login_padres():
    return portal_login('parent')

@app.route('/login')
def login_redirect():
    return redirect(url_for('index'))

@app.route('/login/<portal>', methods=('GET', 'POST'))
def portal_login(portal):
    if request.method == 'POST':
        username, password = request.form['username'].strip(), request.form['password']
        user = execute_query('SELECT * FROM users WHERE username = ?', (username,), fetchone=True)
        
        if user and check_password_hash(user['password'], password):
            # Verificar que el usuario pertenece al portal
            if user['role'] == portal:
                session.clear()
                session['user_id'], session['name'], session['grade'], session['role'] = user['id'], user['name'], user['grade'], user['role']
                return redirect(url_for('index'))
            else:
                flash(f'Este usuario no tiene acceso al Portal de {portal.capitalize()}.', 'error')
        else:
            flash('Credenciales incorrectas.', 'error')
    return render_template('login.html', portal=portal)

@app.route('/register/<portal>', methods=('GET', 'POST'))
def register(portal):
    if request.method == 'POST':
        username, password, name = request.form['username'].strip(), request.form['password'], request.form['name'].strip()
        grade = int(request.form.get('grade', 0))
        
        try:
            execute_query(
                'INSERT INTO users (username, password, name, grade, role) VALUES (?, ?, ?, ?, ?)',
                (username, generate_password_hash(password), name, grade, portal),
                commit=True
            )
            flash('Registro exitoso. ¡Inicia sesión!', 'success')
            return redirect(url_for('portal_login', portal=portal))
        except Exception as e:
            flash(f'Error: El usuario ya existe o datos inválidos.', 'error')
    return render_template('register.html', portal=portal)

@app.route('/dashboard')
def dashboard():
    if session.get('role') != 'student': return redirect(url_for('index'))
    user = execute_query('SELECT score, completed FROM users WHERE id = ?', (session['user_id'],), fetchone=True)
    score, completed = (user['score'], user['completed']) if user else (0.0, 0)
    return render_template('dashboard.html', files=get_files_for_grade(session['grade']), name=session['name'], grade=session['grade'], score=score, completed=completed, animal=get_animal_reward(score))

@app.route('/parent_dashboard')
def parent_dashboard():
    if session.get('role') != 'parent': return redirect(url_for('index'))
    activities = execute_query('SELECT * FROM parent_activities WHERE parent_id = ? ORDER BY created_at DESC', (session['user_id'],), fetchall=True)
    return render_template('parent_dashboard.html', activities=activities, name=session['name'])

@app.route('/create_activity', methods=['POST'])
def create_activity():
    if session.get('role') != 'parent': return redirect(url_for('index'))
    title = request.form['title']
    description = request.form['description']
    normative = request.form['normative']
    grade = request.form['grade']
    
    execute_query(
        'INSERT INTO parent_activities (parent_id, title, description, normative, grade) VALUES (?, ?, ?, ?, ?)',
        (session['user_id'], title, description, normative, grade),
        commit=True
    )
    flash('Actividad creada con éxito según normativa UE.', 'success')
    return redirect(url_for('parent_dashboard'))

@app.route('/admin_dashboard')
def admin_dashboard():
    if session.get('role') != 'teacher': return redirect(url_for('index'))
    grade_filter = request.args.get('grade', type=int)
    query = "SELECT * FROM users WHERE role = 'student'"
    params = ()
    if grade_filter:
        query += ' AND grade = ?'
        params = (grade_filter,)
    query += ' ORDER BY score DESC, completed DESC'
    students = execute_query(query, params, fetchall=True)
    return render_template('admin_dashboard.html', students=students, name=session['name'], selected_grade=grade_filter)

@app.route('/complete_activity', methods=['POST'])
def complete_activity():
    if session.get('role') != 'student': return {'status': 'error'}, 403
    user = execute_query('SELECT score, completed FROM users WHERE id = ?', (session['user_id'],), fetchone=True)
    if user:
        execute_query('UPDATE users SET score = ?, completed = ? WHERE id = ?', (min(5.0, user['score'] + 0.5), user['completed'] + 1, session['user_id']), commit=True)
    return {'status': 'success'}

@app.route('/material/<periodo_id>/<filename>')
def serve_material(periodo_id, filename):
    if not session.get('user_id'): return redirect(url_for('index'))
    if '/' in filename or '\\' in filename: return "Acceso denegado", 403
    return send_from_directory(GUIAS_2P_PATH if periodo_id == '2P' else GUIAS_1P_PATH, filename)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

init_db()

@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=3000)
