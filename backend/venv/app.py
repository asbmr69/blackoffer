from flask import Flask, jsonify, request
from flask_cors  import CORS
from flask_pymongo import PyMongo
import json
from pymongo import MongoClient
from bson.objectid import ObjectId
import os


app = Flask(__name__)

CORS(app)
app.config["MONGO_URI"]="mongodb+srv://asbmr2003:ZSF1nmOBDv6t4hAV@cluster.twp9eli.mongodb.net/blackcoffer?retryWrites=true&w=majority&appName=Cluster"
mongo = PyMongo(app)
db = mongo.db.collection1

# Create a new document
@app.route('/api/data', methods=['POST'])
def create_data():
    data = request.json
    result = db.insert_one(data)
    return jsonify({"_id": str(result.inserted_id)}), 201

# Read all documents
@app.route('/api/data', methods=['GET'])
def get_all_data():
    data = list(db.find())
    for item in data:
        item['_id'] = str(item['_id'])
    return jsonify(data), 200

# Read a single document by ID
@app.route('/api/data/<id>', methods=['GET'])
def get_data(id):
    try:
        data = db.find_one({"_id": ObjectId(id)})
        if data:
            data['_id'] = str(data['_id'])
            return jsonify(data), 200
        else:
            return jsonify({"error": "Data not found"}), 404
    except:
        return jsonify({"error": "Invalid ID format"}), 400

# Update a document by ID
@app.route('/api/data/<id>', methods=['PUT'])
def update_data(id):
    data = request.json
    try:
        result = db.update_one({"_id": ObjectId(id)}, {"$set": data})
        if result.matched_count > 0:
            return jsonify({"message": "Data updated successfully"}), 200
        else:
            return jsonify({"error": "Data not found"}), 404
    except:
        return jsonify({"error": "Invalid ID format"}), 400

# Delete a document by ID
@app.route('/api/data/<id>', methods=['DELETE'])
def delete_data(id):
    try:
        result = db.delete_one({"_id": ObjectId(id)})
        if result.deleted_count > 0:
            return jsonify({"message": "Data deleted successfully"}), 200
        else:
            return jsonify({"error": "Data not found"}), 404
    except:
        return jsonify({"error": "Invalid ID format"}), 400






if __name__ == '__main__':
    app.run(debug =True)
