import json
import os
import time
from flask import Flask, Blueprint, jsonify, request, current_app

files_bp = Blueprint('files', __name__)
app = Flask(__name__)
JSON_FILE_PATH = os.path.join(app.root_path, '../uploads', 'data.json')

# 取得(All)
@files_bp.route('/api/files', methods=['GET'])
def get_files():
    files = read_json()
    return jsonify(files), 200

# 取得
@files_bp.route('/api/files/<int:file_id>', methods=['GET'])
def get_file(file_id):
    files = read_json()
    file = next((file for file in files if file["id"] == file_id), None)
    if file:
        return jsonify(file), 200
    else:
        return jsonify({"error": "Item not found"}), 404

# 刪除
@files_bp.route('/api/files/<int:file_id>', methods=['DELETE'])
def delete_file(file_id):
    files = read_json()

    # 刪除目標檔案
    target = find_json(file_id)
    file_path = 'uploads/' + target["fileName"]
    if os.path.exists(file_path):
        os.remove(file_path)

    # 寫入文字檔
    files = [file for file in files if file["id"] != file_id]
    write_json(files)
    return jsonify({"message": "Item deleted"}), 200

# 檔案上傳
@files_bp.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # 將檔案資訊寫入data.json
    nowFilesData = read_json()
    new_file = {"id": get_new_id(), "fileName": file.filename, "uploadedAt":  int(time.time()), "fileType": 1, "status":1}
    nowFilesData.append(new_file)  
    write_json(nowFilesData)

    # 儲存檔案到上傳資料夾
    upload_folder = os.path.join(current_app.root_path, 'uploads')
    os.makedirs(upload_folder, exist_ok=True)
    file_path = os.path.join(upload_folder, file.filename)
    file.save(file_path)

    return jsonify({"message": "File uploaded successfully!", "file_path": file_path}), 201


###############

# 測試
@files_bp.route('/api/test', methods=['GET'])
def test():
    testData = [
        {"id": 1, "fileName": "testFile_1", "uploadedAt": 1630096372, "fileType": 1, "status":1},
        {"id": 2, "fileName": "testFile_2", "uploadedAt": 1630196372, "fileType": 1, "status":2},
        {"id": 3, "fileName": "testFile_3", "uploadedAt": 1630056372, "fileType": 1, "status":3},
        {"id": 4, "fileName": "testFile_4", "uploadedAt": 1630022372, "fileType": 1, "status":9},
        {"id": 5, "fileName": "testFile_5", "uploadedAt": 1730096372, "fileType": 1, "status":2},
    ]
    write_json(testData)
    return jsonify({"message": "Done"}), 200

def find_json(file_id):
    files = read_json()
    result = next((item for item in files if item["id"] == file_id), None)
    return result

def read_json():
    # 檢查檔案是否存在
    if not os.path.exists(JSON_FILE_PATH):
        os.makedirs(os.path.dirname(JSON_FILE_PATH), exist_ok=True)
        with open(JSON_FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump([], f, indent=4)
    
    # 檔案存在，讀取資料
    with open(JSON_FILE_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def write_json(data):
    # 檢查檔案是否存在
    if not os.path.exists(JSON_FILE_PATH):
        os.makedirs(os.path.dirname(JSON_FILE_PATH), exist_ok=True)
        with open(JSON_FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump({"items": []}, f, indent=4)

    with open(JSON_FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def get_new_id():
    nowFilesData = read_json()
    return max((item["id"] for item in nowFilesData), default=0) + 1