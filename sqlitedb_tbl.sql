--
-- File generated with SQLiteStudio v3.4.20 on 週二 一月 20 16:43:31 2026
--
-- Text encoding used: UTF-8
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: bugs
DROP TABLE IF EXISTS bugs;

CREATE TABLE IF NOT EXISTS bugs (
    id                  INTEGER  PRIMARY KEY AUTOINCREMENT,
    report_date         DATETIME DEFAULT CURRENT_TIMESTAMP,-- 報告時間，自動填入目前時間
    system              TEXT     NOT NULL,-- 系統或模組名稱
    bug_details         TEXT     NOT NULL,-- 錯誤詳細描述
    reported_by         TEXT     NOT NULL,-- 報告者
    status              TEXT     DEFAULT '開放中',-- 狀態：開放中、處理中、已解決、已關閉
    priority            TEXT     DEFAULT '中',-- 優先級：低、中、高
    severity            TEXT     DEFAULT '中',-- 嚴重程度：輕微、中、重大、嚴重
    assigned_to         TEXT,-- 指派給誰（可為空）
    resolution_date     DATETIME,-- 解決時間
    notes               TEXT/* 備註或更新記錄 */,
    reported_by_user_id INTEGER  REFERENCES users (id) 
);

INSERT INTO bugs (id, report_date, system, bug_details, reported_by, status, priority, severity, assigned_to, resolution_date, notes, reported_by_user_id) VALUES (2, '2026-01-09 01:14:24', 'eSHOP', 'Pop up password need to change', 'Yung', '已解決', '高', '嚴重', '', '2026-01-12 15:06:58', 'scheduled : 10/1 00:00 changed new password
completed the pop up password update.', NULL);
INSERT INTO bugs (id, report_date, system, bug_details, reported_by, status, priority, severity, assigned_to, resolution_date, notes, reported_by_user_id) VALUES (4, '2026-01-09 09:23:10', 'M18', 'Location  issues', 'Connie', '已解決', '低', '中', 'IT', '2026-01-12 15:06:17', 'Schedule 12/1 13:00-13:30 reboot server.
After reboot. and config.  resolved for location issues.', 2);
INSERT INTO bugs (id, report_date, system, bug_details, reported_by, status, priority, severity, assigned_to, resolution_date, notes, reported_by_user_id) VALUES (5, '2026-01-13 00:55:16', 'eShop', 'Staging frontend and admin portal  blank page', 'IT', '已解決', '低', '輕微', 'Mirco', NULL, 'resolved', 2);

-- Table: users
DROP TABLE IF EXISTS users;

CREATE TABLE IF NOT EXISTS users (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    username      TEXT    UNIQUE
                          NOT NULL,
    password_hash TEXT    NOT NULL,
    is_admin      BOOLEAN DEFAULT 0
);

INSERT INTO users (id, username, password_hash, is_admin) VALUES (1, 'admin', 'scrypt:32768:8:1$aD25sHWDsUxya0h3$822521bf77d75402d339773b32e36819068ce165428ac50ecb02bbb350929ca77da0aded42752489e4bf460a4c61059b4986662541f1afd08c0344edc06756fe', 1);
INSERT INTO users (id, username, password_hash, is_admin) VALUES (2, 'it', 'scrypt:32768:8:1$TrQY8tmSLOFDaD6P$6c36bb3fa8c11f47403a85d5c4101c4d92d32b11c0a51946254f083ec5df206aabe6d5e81d1db5e480c10eb168d1c095488ce38d4c0b2f2132690d94d968cf97', 1);
INSERT INTO users (id, username, password_hash, is_admin) VALUES (3, 'mkt', 'scrypt:32768:8:1$oMURZ2XX1LbegxJ4$d564e70171a4a8c5544f4d85a2391403a83a85cdaf2442096a66055bea5a147bd66382813a894f3e1f9a3b5b1798534e661fe20d2e33d761432b2b99c5650d4d', 0);
INSERT INTO users (id, username, password_hash, is_admin) VALUES (4, 'itadmin', 'scrypt:32768:8:1$TrQY8tmSLOFDaD6P$6c36bb3fa8c11f47403a85d5c4101c4d92d32b11c0a51946254f083ec5df206aabe6d5e81d1db5e480c10eb168d1c095488ce38d4c0b2f2132690d94d968cf97', 1);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
