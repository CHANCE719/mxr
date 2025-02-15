from flask import Flask, render_template, request, redirect, url_for, flash, render_template_string
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = '111'
app = Flask(__name__, static_folder='static')
app.config['TEMPLATES_AUTO_RELOAD'] = True

# 数据库连接配置
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',  # 数据库主机地址
            user='root',  # 数据库用户名
            password='Asdf1234',  # 数据库密码
            database='userdb',  # 数据库名称
            connection_timeout=30)

        if connection.is_connected():
            print("Connected to MySQL database")
            return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'register':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']

            connection = get_db_connection()
            cursor = connection.cursor()

            try:
                password_hash = generate_password_hash(password)
                insert_query = """
                INSERT INTO users (username, email, password_hash) 
                VALUES (%s, %s, %s)
                """
                cursor.execute(insert_query, (username, email, password_hash))
                connection.commit()
                flash('User registered successfully!', 'success')
                return redirect(url_for('login'))  # 注册成功后跳转到登录界面
            except mysql.connector.Error as error:
                flash(f'Failed to register user: {error}', 'danger')
            finally:
                cursor.close()
                connection.close()

        elif action == 'login':
            email = request.form['email']
            password = request.form['password']

            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)

            try:
                select_query = "SELECT id, username, password_hash FROM users WHERE email=%s"
                cursor.execute(select_query, (email,))
                user = cursor.fetchone()

                if user and check_password_hash(user['password_hash'], password):
                    flash('Login successful!', 'success')
                else:
                    flash('Invalid credentials.', 'danger')
            except mysql.connector.Error as error:
                flash(f'Failed to login: {error}', 'danger')
            finally:
                cursor.close()
                connection.close()

    return render_template('index.html')

# 初始化数据库表
def init_db():
    connection = get_db_connection()
    cursor = connection.cursor()

    # 创建用户表
    create_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) NOT NULL,
        email VARCHAR(100) NOT NULL UNIQUE,
        password_hash VARCHAR(255) NOT NULL
    )
    """
    cursor.execute(create_table_query)
    connection.commit()
    cursor.close()
    connection.close()

# 在第一次请求前初始化数据库
@app.before_request
def before_request():
    init_db()

# 注册处理函数
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        try:
            password_hash = generate_password_hash(password)
            insert_query = """
            INSERT INTO users (username, email, password_hash) 
            VALUES (%s, %s, %s)
            """
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute(insert_query, (username, email, password_hash))
            connection.commit()
            cursor.close()
            connection.close()
            flash('User registered successfully!', 'success')
            return redirect(url_for('login'))  # 注册成功后跳转到登录界面
        except mysql.connector.Error as e:
            flash(f'Failed to register user: {e}', 'danger')
        except Exception as e:
            flash(f'An error occurred: {e}', 'danger')
    return render_template_string('''
        <form method="post">
            Username: <input type="text" name="username"><br>
            Email: <input type="email" name="email"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Register">
        </form>
    ''')

# 登录处理函数
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            select_query = "SELECT id, username, password_hash FROM users WHERE email=%s"
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(select_query, (email,))
            user = cursor.fetchone()

            if user and check_password_hash(user['password_hash'], password):
                flash('Login successful!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Invalid credentials.', 'danger')
            cursor.close()
            connection.close()
        except mysql.connector.Error as error:
            flash(f'Failed to login: {error}', 'danger')
    return render_template_string('''
        <form method="post">
            Email: <input type="email" name="email"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    ''')

@app.route('/')
def home():
    return "Welcome to the Home Page!"

if __name__ == '__main__':
    app.run(debug=True)