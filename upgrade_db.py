import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect('bug_tracker.db')
cursor = conn.cursor()

# 建立 users 表
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    is_admin BOOLEAN DEFAULT 0
)
''')

# 在 bugs 表新增 reported_by_user_id 欄位（允許 NULL，舊資料相容）
cursor.execute('''
ALTER TABLE bugs ADD COLUMN reported_by_user_id INTEGER REFERENCES users(id)
''')

# 建立預設管理員帳號（使用者名稱: admin，密碼: 請自行修改）
admin_password = "YourStrongAdminPassword2026"  # <<< 請改成您要的密碼
cursor.execute('''
INSERT OR IGNORE INTO users (username, password_hash, is_admin)
VALUES (?, ?, 1)
''', ('admin', generate_password_hash(admin_password)))

# 可再新增一般使用者範例（選用）
# cursor.execute('INSERT OR IGNORE INTO users (username, password_hash, is_admin) VALUES (?, ?, 0)',
#                ('user1', generate_password_hash('user123')))

conn.commit()
conn.close()
print("資料庫升級完成！預設管理員帳號：admin / 密碼：您剛剛設定的")