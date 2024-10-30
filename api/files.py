import json
import os
import time
import sqlite3
# from enum import Enum
from flask import Flask, Blueprint, jsonify, request, current_app

app = Flask(__name__)
files_bp = Blueprint('files', __name__)
JSON_FILE_PATH = os.path.join(app.root_path, '../uploads', 'data.json')

# class FileType(Enum):
#     PDF = 1

# class Status(Enum):
#     Uploading = 1
#     Parsing = 2
#     Completed = 3
#     Failed = 9

# 取得(All)
@files_bp.route('/api/files', methods=['GET'])
def get_files():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM files')
    files = cursor.fetchall()
    conn.close()

    return jsonify([dict(file) for file in files]), 200

# 取得
@files_bp.route('/api/files/<int:file_id>', methods=['GET'])
def get_file(file_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM files WHERE id = ?', (file_id,))
    file = cursor.fetchone()
    conn.close()

    if file is None:
        return jsonify({'message': 'File not found!'}), 404

    return jsonify(dict(file)), 200
    
# 新增
@files_bp.route('/api/files', methods=['POST'])
def insert_file():
    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400
    
    # 將檔案資訊寫入DB
    file_name = file.filename
    uploaded_at = int(time.time())
    file_type = 1
    status = 1 # Uploading

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO files (fileName, uploadedAt, fileType, status) VALUES (?, ?, ?, ?)',(file_name, uploaded_at, file_type, status))
    conn.commit()

    cursor.execute('SELECT id FROM files WHERE fileName = ?', (file_name,))
    newId = cursor.fetchone()['id']

    conn.close()

    return jsonify({"message": "Insert successfully！", "data": newId}), 201


# 刪除
@files_bp.route('/api/files/<int:file_id>', methods=['DELETE'])
def delete_file(file_id):

    # 刪除目標檔案
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT fileName FROM files WHERE id = ?', (file_id,))
    file = cursor.fetchone()

    file_path = 'uploads/' + file["fileName"]
    if os.path.exists(file_path):
        os.remove(file_path)

    # 寫入DB
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM files WHERE id = ?', (file_id,))
    conn.commit()
    conn.close()

    time.sleep(2) # 模擬耗時
    return jsonify({"message": "File deleted"}), 200

# Upload
@files_bp.route('/api/upload/<int:file_id>', methods=['POST'])
def upload_file(file_id):
    if file_id is None:
        return jsonify({"message": "File not found."}), 400

    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400
    
    # 儲存檔案到上傳資料夾
    upload_folder = os.path.join(current_app.root_path, 'uploads')
    os.makedirs(upload_folder, exist_ok=True)
    file_path = os.path.join(upload_folder, file.filename)
    file.save(file_path)

    time.sleep(2) # 模擬耗時

    if not os.path.exists(file_path):
        return jsonify({"message": "Uploaded failed！"}), 500
    
    # 寫入DB
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('UPDATE files SET status = ? WHERE id = ?', (2, file_id))
        conn.commit()
        return jsonify({"message": "Uploaded successfully！"}), 200
    except sqlite3.IntegrityError:
        return jsonify({'message': 'File name must be unique!'}), 400
    finally:
        conn.close()


# Parse
@files_bp.route('/api/parse/<int:file_id>', methods=['POST'])
def parse_file(file_id):
    
    # # 查找並更新目標物件
    # files = read_json()
    # for file in files:
    #     if file["id"] == file_id:
    #         # TODO::執行parsing

    #         file["status"] = 3
    #         write_json(files)
    #         return jsonify({"message": "Parsing successfully.", "file": file}), 200
    # return jsonify({"message": "File not found."}), 400

    # 寫入DB    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('UPDATE files SET status = ? WHERE id = ?', (3, file_id))
        conn.commit()

        time.sleep(3) # 模擬耗時
        return jsonify({"message": "Parsing successfully."}), 200
    except sqlite3.IntegrityError:
        return jsonify({'message': 'File name must be unique!'}), 400
    finally:
        conn.close()

    
###############

# 測試
@files_bp.route('/api/test', methods=['GET'])
def test():
    create_table()
    
    return jsonify({"message": "Done"}), 200

def create_table():
    if not os.path.exists('uploads/'):
        os.makedirs('uploads/', exist_ok=True)

    # 連接到數據庫，或創建名為 `project.db` 的數據庫文件
    conn = sqlite3.connect('uploads/project.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fileName TEXT NOT NULL UNIQUE,
        uploadedAt INTEGER NOT NULL,
        fileType INTEGER NOT NULL,
        status INTEGER NOT NULL
    )
    ''')
    conn.commit()  # 確保保存修改
    conn.close()
    return

def get_db_connection():
    if not os.path.exists('uploads/project.db'):
        create_table()
    
    conn = sqlite3.connect('uploads/project.db')
    conn.row_factory = sqlite3.Row  # 這樣可以通過列名訪問行數據
    return conn