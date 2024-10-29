from flask import Blueprint, jsonify, request

files_bp = Blueprint('files', __name__)

# 模擬的資料庫（使用列表作為資料儲存）
files = [
    {"id": 1, "fileName": "testFile_1", "uploadedAt": 1630096372, "fileType": 1, "status":1},
    {"id": 2, "fileName": "testFile_2", "uploadedAt": 1630196372, "fileType": 1, "status":2},
    {"id": 3, "fileName": "testFile_3", "uploadedAt": 1630056372, "fileType": 1, "status":3},
    {"id": 4, "fileName": "testFile_4", "uploadedAt": 1630022372, "fileType": 1, "status":9},
    {"id": 5, "fileName": "testFile_5", "uploadedAt": 1730096372, "fileType": 1, "status":2},
]

# 取得所有項目
@files_bp.route('/api/files', methods=['GET'])
def get_files():
    return jsonify(files), 200

# 取得
@files_bp.route('/api/files/<int:file_id>', methods=['GET'])
def get_file(file_id):
    file = next((file for file in files if file["id"] == file_id), None)
    if file:
        return jsonify(file), 200
    else:
        return jsonify({"error": "Item not found"}), 404

# 新增
@files_bp.route('/api/files', methods=['POST'])
def add_file():
    new_file = request.get_json()
    new_file['id'] = len(files) + 1  # 簡單的 ID 自增方法
    files.append(new_file)
    return jsonify(new_file), 201

# 更新
@files_bp.route('/api/files/<int:file_id>', methods=['PUT'])
def update_file(file_id):
    file = next((file for file in files if file["id"] == file_id), None)
    if file:
        data = request.get_json()
        file.update(data)
        return jsonify(file), 200
    else:
        return jsonify({"error": "Item not found"}), 404

# 刪除
@files_bp.route('/api/files/<int:file_id>', methods=['DELETE'])
def delete_file(file_id):
    global files
    files = [file for file in files if file["id"] != file_id]
    return jsonify({"message": "Item deleted"}), 200
