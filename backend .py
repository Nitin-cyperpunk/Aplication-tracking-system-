from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/myapp"
mongo = PyMongo(app)
CORS(app)  # Enable CORS for cross-origin requests

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']

    user = mongo.db.users.find_one({'username': username, 'password': password})

    if user:
        return jsonify({'paymentStatus': user['paymentStatus']})
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/upload', methods=['POST'])
def upload_document():
    username = request.form['username']
    password = request.form['password']

    user = mongo.db.users.find_one({'username': username, 'password': password})

    if user:
        file = request.files['document']
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        mongo.db.users.update_one({'_id': user['_id']}, {'$push': {'documents': file_path}})

        return jsonify({'message': 'Document uploaded successfully'})
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)