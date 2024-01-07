import sqlite3

# データベースに接続（存在しない場合は新規作成）
conn = sqlite3.connect('arsenal_fan_club.db')

# votes テーブルの作成
with conn:
    conn.execute('''
    CREATE TABLE IF NOT EXISTS votes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_id INTEGER,
        vote_time TEXT,
        FOREIGN KEY (player_id) REFERENCES players(id)
    )
    ''')

# 接続を閉じる
conn.close()
