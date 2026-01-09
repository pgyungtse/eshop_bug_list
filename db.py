import sqlite3
from datetime import datetime

# 資料庫檔案名稱
DB_NAME = "bug_tracker.db"

# 連接到 SQLite 資料庫（如果檔案不存在會自動建立）
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# 建立 bugs 資料表
cursor.execute('''
CREATE TABLE IF NOT EXISTS bugs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    report_date DATETIME DEFAULT CURRENT_TIMESTAMP,  -- 報告時間，自動填入目前時間
    system TEXT NOT NULL,                            -- 系統或模組名稱
    bug_details TEXT NOT NULL,                       -- 錯誤詳細描述
    reported_by TEXT NOT NULL,                       -- 報告者
    status TEXT DEFAULT '開放中',                     -- 狀態：開放中、處理中、已解決、已關閉
    priority TEXT DEFAULT '中',                      -- 優先級：低、中、高
    severity TEXT DEFAULT '中',                      -- 嚴重程度：輕微、中、重大、嚴重
    assigned_to TEXT,                                -- 指派給誰（可為空）
    resolution_date DATETIME,                        -- 解決時間
    notes TEXT                                       -- 備註或更新記錄
)
''')

# 提交變更並關閉連線
conn.commit()
conn.close()

print(f"資料庫 '{DB_NAME}' 建立成功！")
print("資料表 'bugs' 已建立，欄位如下：")
print("""
- id (自動編號)
- report_date (報告日期時間，預設目前時間)
- system (系統名稱)
- bug_details (錯誤細節)
- reported_by (報告者)
- status (狀態，預設 '開放中')
- priority (優先級，預設 '中')
- severity (嚴重程度，預設 '中')
- assigned_to (指派人員)
- resolution_date (解決日期時間)
- notes (備註)
""")

# 可選：插入一筆測試資料
def insert_test_data():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO bugs (
        system, bug_details, reported_by, status, priority, severity, assigned_to, notes
    ) VALUES (
        '登入模組', '使用者登入時偶爾出現 500 錯誤', '張小明', '處理中', '高', '重大', '李工程師', '已重現問題，正在排查資料庫連線'
    )
    ''')
    
    conn.commit()
    conn.close()
    print("已插入一筆測試資料！")

# 取消註解下面這行即可插入測試資料
# insert_test_data()