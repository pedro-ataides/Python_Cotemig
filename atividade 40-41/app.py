import sqlite3
import requests
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.secret_key = 's'

# --- Conexão e Banco de Dados ---
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT,
            status TEXT DEFAULT 'Pendente',
            usuario_id INTEGER,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# --- Decorator de Autenticação ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# --- Rotas de Autenticação ---
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = generate_password_hash(request.form['senha'])

        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)', (nome, email, senha))
            conn.commit()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            return "Email já cadastrado!", 400
        finally:
            conn.close()
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM usuarios WHERE email = ?', (email,)).fetchone()
        conn.close()

        if user and check_password_hash(user['senha'], senha):
            session['usuario_id'] = user['id']
            session['usuario_nome'] = user['nome']
            return redirect(url_for('dashboard'))
        return "Credenciais inválidas!", 401

    return render_template('login.html')





@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# --- Rotas da Aplicação (Dashboard e CRUD) ---
@app.route('/')
@app.route('/dashboard')
@login_required
def dashboard():
    # Integração com API externa
    quote = "Mantenha o foco!"
    try:
        response = requests.get('https://api.adviceslip.com/advice', timeout=3)
        if response.status_code == 200:
            quote = response.json()['slip']['advice']
    except:
        pass

    return render_template('dashboard.html', quote=quote)

@app.route('/nova_tarefa', methods=['GET', 'POST'])
@login_required
def nova_tarefa():
    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        status = request.form.get('status', 'Pendente')

        conn = get_db_connection()
        conn.execute('INSERT INTO tarefas (titulo, descricao, status, usuario_id) VALUES (?, ?, ?, ?)',
                     (titulo, descricao, status, session['usuario_id']))
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))

    return render_template('task_form.html', task=None)

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_tarefa(id):
    conn = get_db_connection()
    task = conn.execute('SELECT * FROM tarefas WHERE id = ? AND usuario_id = ?', (id, session['usuario_id'])).fetchone()

    if not task:
        conn.close()
        return "Tarefa não encontrada", 4404

    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        status = request.form['status']

        conn.execute('UPDATE tarefas SET titulo = ?, descricao = ?, status = ? WHERE id = ?',
                     (titulo, descricao, status, id))
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))

    conn.close()
    return render_template('task_form.html', task=task)

@app.route('/excluir/<int:id>', methods=['POST', 'DELETE'])
@login_required
def excluir_tarefa(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM tarefas WHERE id = ? AND usuario_id = ?', (id, session['usuario_id']))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

# --- Rota Avançada: API REST & Progresso ---
@app.route('/api/tarefas')
@login_required
def api_tarefas():
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tarefas WHERE usuario_id = ?', (session['usuario_id'],)).fetchall()
    conn.close()
    return jsonify([dict(t) for t in tasks])

@app.route('/progresso')
@login_required
def progresso():
    return render_template('progress.html')

if __name__ == '__main__':
    app.run(debug=True)