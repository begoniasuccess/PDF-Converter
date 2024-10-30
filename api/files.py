import json
import os
import time
from enum import Enum
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
        return jsonify({"message": "Item not found"}), 404
    
# 新增
@files_bp.route('/api/files', methods=['POST'])
def insert_file():
    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400
    
    # 將檔案資訊寫入data.json
    nowFilesData = read_json()
    new_file = {"id": get_new_id(), "fileName": file.filename, "uploadedAt":  int(time.time()), "fileType": 1, "status":1} # Uploading
    nowFilesData.append(new_file)  
    write_json(nowFilesData)

    return jsonify({"message": "Insert successfully！", "data": new_file['id']}), 201


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
    
    # 將檔案資訊寫入data.json
    files = read_json()
    for file in files:
        if file["id"] == file_id:
            file["status"] = 2 # Parsing
            write_json(files)

    return jsonify({"message": "Uploaded successfully！"}), 200

# Parse
@files_bp.route('/api/parse/<int:file_id>', methods=['POST'])
def parse_file(file_id):
    files = read_json()

    # 查找並更新目標物件
    for file in files:
        if file["id"] == file_id:
            # TODO::執行parsing
            time.sleep(3) # 模擬耗時

            file["status"] = 3
            write_json(files)
            return jsonify({"message": "Parsing successfully.", "file": file}), 200

    
    return jsonify({"message": "File not found."}), 400

###############

# 測試
@files_bp.route('/api/test', methods=['GET'])
def test():
    # testData = [
    #     {"id": 1, "fileName": "testFile_1", "uploadedAt": 1630096372, "fileType": 1, "status":1},
    #     {"id": 2, "fileName": "testFile_2", "uploadedAt": 1630196372, "fileType": 1, "status":2},
    #     {"id": 3, "fileName": "testFile_3", "uploadedAt": 1630056372, "fileType": 1, "status":3},
    #     {"id": 4, "fileName": "testFile_4", "uploadedAt": 1630022372, "fileType": 1, "status":9},
    #     {"id": 5, "fileName": "testFile_5", "uploadedAt": 1730096372, "fileType": 1, "status":2},
    # ]
    # write_json(testData)
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