from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
import re
from datetime import datetime
import urllib.request
import json

# Flaskアプリケーションの初期化
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# データベースファイルのパス
DATABASE = 'membersite.db'

# データベースに接続するためのヘルパー関数
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# ログインページ
@app.route('/login', methods=['POST'])
def login():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        account = cursor.fetchone()
        conn.close()

        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            return redirect(url_for('index'))  # ログイン後にindexページへリダイレクト
        else:
            msg = 'Incorrect username/password!'
    return render_template('login.html', msg=msg)

# ログアウトページ
@app.route('/logout/')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

# 登録ページ
@app.route('/register/', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? OR email = ?', (username, email))
        account = cursor.fetchone()

        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        else:
            cursor.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', (username, email, password))
            conn.commit()
            msg = 'You have successfully registered!'
            conn.close()
            return redirect(url_for('index'))  # 登録後にindexページへリダイレクト
    return render_template('register.html', msg=msg)

# ホームページ
@app.route('/')
def home():
    if 'loggedin' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))

# インデックスページ
@app.route('/index/')
def index():
    if 'loggedin' in session:
        return render_template('index.html', username=session['username'])
    return redirect(url_for('login'))

# sub01ページ
@app.route('/sub01/')
def sub01():
    # ユーザーがログインしているかチェック
    if 'loggedin' in session:
        # データベースから選手のデータを取得
        conn = sqlite3.connect('arsenal_fan_club.db')
        conn.row_factory = sqlite3.Row
        players = conn.execute('SELECT * FROM players').fetchall()
        conn.close()
        
        # 選手のデータをテンプレートに渡す
        return render_template('sub01.html', players=players)
    else:
        # ログインしていない場合はログインページにリダイレクト
        return redirect(url_for('login'))


#投票システム
@app.route('/vote_for_mvp/', methods=['POST'])
def vote_for_mvp():
    player_id = request.form['player_id']
    vote_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn = get_db_connection()
    conn.execute('INSERT INTO votes (player_id, vote_time) VALUES (?, ?)', (player_id, vote_time))
    conn.commit()

    results = get_voting_results(conn)
    conn.close()
    return jsonify({'results': results})

def get_voting_results(conn):
    results = conn.execute('''
        SELECT p.name, COUNT(v.player_id) as vote_count
        FROM votes v
        JOIN players p ON v.player_id = p.id
        GROUP BY v.player_id
    ''').fetchall()

    results_html = ''.join([f"<p>{result['name']}: {result['vote_count']} votes</p>" for result in results])
    return results_html


#API機能
@app.route('/arsenal-info/')
def arsenal_info():
    url = "http://api.football-data.org/v4/teams/57/"
    headers = {"X-Auth-Token": "ef77d54e77f34b2caf203eecc833584e"}  # 自分のAPIキー

    # APIリクエストを送信
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read())

    # レスポンスデータをテンプレートに渡す
    return render_template('info.html', data=data)


@app.route('/sub02')
def sub02():
    # sub02.htmlをレンダリングする
    return render_template('sub02.html')

#Ajaxの機能
# コメントリスト
commentaries = []

@app.route('/submit-commentary', methods=['POST'])
def submit_commentary():
    data = request.get_json()
    commentary = data.get('commentary')
    # コメントをリストに追加
    commentaries.insert(0, commentary)
    return jsonify({'commentary': commentary})

@app.route('/get-commentaries', methods=['GET'])
def get_commentaries():
    # コメントリストを返す
    return jsonify({'commentaries': commentaries})


# アプリケーションの実行
if __name__ == '__main__':
    app.run(debug=True)
