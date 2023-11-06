from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3

app = Flask(__name)

# データベースに接続
conn = sqlite3.connect('user.db')
cursor = conn.cursor()

# テーブルが存在しない場合は作成
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT,
        password TEXT
    )
''')

# ダミーデータとしてユーザーを登録
cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ("user", "password"))
conn.commit()

# ユーザーのログイン情報を検証
def verify_login(username, password):
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    return user is not None

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if verify_login(username, password):
        # ログイン成功時にindex.htmlにリダイレクト
        return redirect(url_for('index'))
    else:
        response = {"message": "failure"}
        return jsonify(response)

@app.route('/index')
def index():
    # index.html ページの表示
    return render_template('index.html')

@app.route('/post-comment', methods=['POST'])
def post_comment():
    data = request.get_json()
    comment_text = data.get('comment')
    # コメントを保存するためのコード
    # 保存が成功した場合は {"success": true} を返す
    response = {"success": True}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)

# データベースをクローズ
conn.close()
