import sqlite3

# データベースに接続（存在しない場合は新規作成）
conn = sqlite3.connect('arsenal_fan_club.db')

# players テーブルの作成
with conn:
    conn.execute('''
    CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    ''')

    # 出場選手データの追加
    players = [
        ('ラムズデール', ),
        ('ベン ホワイト', ),
        ('サリバ', ),
        ('ガブリエウ', ),
        ('キヴオル', ),
        ('ジョルジーニョ', ),
        ('ウーデゴール', ),
        ('デクラン ライス', ),
        ('サカ', ),
        ('ハヴァーツ', ),
        ('ネルソン', ),
        ('マルティネッリ',)
    ]
    conn.executemany('INSERT INTO players (name) VALUES (?)', players)

# 接続を閉じる
conn.close()
