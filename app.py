from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')

if not app.secret_key or not ADMIN_PASSWORD:
    raise ValueError("請檢查 .env 檔案，SECRET_KEY 和 ADMIN_PASSWORD 必須設定！")

def get_db_connection():
    conn = sqlite3.connect('bug_tracker.db')
    conn.row_factory = sqlite3.Row
    return conn

def is_admin():
    return session.get('admin_logged_in', False)

# 首頁
@app.route('/', methods=['GET'])
def index():
    query = request.args.get('query', '')
    conn = get_db_connection()
    if query:
        bugs = conn.execute('''
            SELECT * FROM bugs 
            WHERE bug_details LIKE ? OR system LIKE ? OR notes LIKE ?
            ORDER BY report_date DESC
        ''', (f'%{query}%', f'%{query}%', f'%{query}%')).fetchall()
    else:
        bugs = conn.execute('SELECT * FROM bugs ORDER BY report_date DESC').fetchall()
    conn.close()
    return render_template('index.html', bugs=bugs, query=query, is_admin=is_admin())

# 新增錯誤
@app.route('/add', methods=['GET', 'POST'])
def add_bug():
    if request.method == 'POST':
        system = request.form['system'].strip()
        bug_details = request.form['bug_details'].strip()
        reported_by = request.form['reported_by'].strip()
        status = request.form['status']
        priority = request.form['priority']
        severity = request.form['severity']
        assigned_to = request.form.get('assigned_to', '').strip()
        notes = request.form.get('notes', '').strip()

        if status in ['已解決', '已關閉'] and not notes:
            flash('當狀態設為「已解決」或「已關閉」時，必須填寫備註說明解決方式或關閉原因！', 'error')
            return render_template('add.html', form_data=request.form, is_admin=is_admin())

        conn = get_db_connection()
        conn.execute('''
            INSERT INTO bugs (system, bug_details, reported_by, status, priority, severity, assigned_to, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (system, bug_details, reported_by, status, priority, severity, assigned_to, notes))
        conn.commit()
        conn.close()
        flash('錯誤記錄新增成功！')
        return redirect(url_for('index'))
    
    return render_template('add.html', is_admin=is_admin())

# 編輯錯誤
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_bug(id):
    if not is_admin():
        flash('僅管理員可編輯記錄！請先登入。', 'error')
        return redirect(url_for('index'))

    conn = get_db_connection()
    bug = conn.execute('SELECT * FROM bugs WHERE id = ?', (id,)).fetchone()
    
    if bug is None:
        flash('找不到該錯誤記錄！')
        conn.close()
        return redirect(url_for('index'))

    if bug['status'] in ['已解決', '已關閉']:
        flash(f'此錯誤記錄已「{bug["status"]}」，無法再進行編輯！', 'error')
        conn.close()
        return redirect(url_for('index'))

    if request.method == 'POST':
        system = request.form['system'].strip()
        bug_details = request.form['bug_details'].strip()
        reported_by = request.form['reported_by'].strip()
        status = request.form['status']
        priority = request.form['priority']
        severity = request.form['severity']
        assigned_to = request.form.get('assigned_to', '').strip()
        notes = request.form.get('notes', '').strip()

        if status in ['已解決', '已關閉'] and not notes:
            flash('當狀態設為「已解決」或「已關閉」時，必須填寫備註！', 'error')
            conn.close()
            return render_template('edit.html', bug=dict(bug), form_data=request.form, is_admin=is_admin())

        resolution_date = bug['resolution_date']
        if bug['status'] not in ['已解決', '已關閉'] and status in ['已解決', '已關閉']:
            resolution_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        conn.execute('''
            UPDATE bugs 
            SET system = ?, bug_details = ?, reported_by = ?, status = ?, priority = ?, severity = ?, 
                assigned_to = ?, notes = ?, resolution_date = ?
            WHERE id = ?
        ''', (system, bug_details, reported_by, status, priority, severity, assigned_to, notes, resolution_date, id))
        conn.commit()
        conn.close()
        flash('錯誤記錄更新成功！')
        return redirect(url_for('index'))
    
    conn.close()
    return render_template('edit.html', bug=bug, is_admin=is_admin())

# 刪除錯誤
@app.route('/delete/<int:id>', methods=['POST'])
def delete_bug(id):
    if not is_admin():
        flash('僅管理員可刪除記錄！', 'error')
        return redirect(url_for('index'))

    conn = get_db_connection()
    conn.execute('DELETE FROM bugs WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('錯誤記錄刪除成功！')
    return redirect(url_for('index'))

# 管理員登入
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        password = request.form['password']
        if password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            flash('管理員登入成功！', 'success')
            return redirect(url_for('index'))
        else:
            flash('密碼錯誤！', 'error')
    
    return render_template('admin_login.html', is_admin=is_admin())

# 管理員登出
@app.route('/admin_logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    flash('已成功登出管理員帳號。')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)