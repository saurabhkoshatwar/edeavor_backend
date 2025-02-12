from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient, errors
from bson.json_util import dumps
import json
import os 

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
MONGODB_URI = os.getenv('MONGODB_URI')

# MongoDB connection setup
try:
    print(MONGODB_URI)
    client = MongoClient(MONGODB_URI)  
    db = client['project1']  # Database name
    collection = db['orders']      # Collection name
except errors.ServerSelectionTimeoutError as err:
    print(f"Error: Could not connect to MongoDB: {err}")
    exit(1)

@app.route('/api/orders', methods=['POST'])
def add_orders():
    try:
        data = json.loads(request.data)

        if not data:
            return jsonify({"error": "No data provided."}), 400

        # Create a document to insert
        document = {"list_order": data['orders']}

        # Insert document into MongoDB
        result = collection.insert_one(document)

        return jsonify({"message": "Orders saved successfully.", "id": str(result.inserted_id)}), 201

    except errors.PyMongoError as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

@app.route('/api/orders', methods=['GET'])
def get_orders():
    try:
        orders = list(collection.find())
        return dumps(orders), 200
    except errors.PyMongoError as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
