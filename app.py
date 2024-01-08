from flask import Flask, render_template, request, jsonify, redirect, url_for

app = Flask(__name__)

# サンプルのユーザ名とパスワード
sample_username = "user"
sample_password = "password"

@app.route('/')
def login_page():
    return render_template('login.html')

#@app.route("/make", methods=["GET", "POST"])
#def make():

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username == sample_username and password == sample_password:
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