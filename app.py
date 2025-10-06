import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.errors import InvalidId

# Load environment variables from .env file
load_dotenv()

# --- Initialize Flask App and Database Connection ---
app = Flask(__name__)

# Get the Connection String from the .env file
uri = os.getenv("MONGO_URI")
if not uri:
    raise ValueError("MONGO_URI is not set in the environment variables. Please check your .env file.")

# Set up the MongoDB Client
try:
    client = MongoClient(uri)
    db = client.bikedb  # Use the database named 'bikedb'
    bikes_collection = db.bikes  # Use the collection named 'bikes'
    # Send a ping to confirm a successful connection
    client.admin.command('ping')
    print("Successfully connected to MongoDB Atlas!")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    client = None

# --- Helper Function for JSON conversion ---
# MongoDB's _id is an ObjectId, which is not directly JSON serializable.
def serialize_doc(doc):
    if doc and "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc

# --- API Routes ---

@app.route('/')
def index():
    """Serves the welcome message and API documentation."""
    return jsonify({
        "message": "Welcome to the Bike Shop API!",
        "api_endpoints": {
            "get_all_or_create_bike": {
                "url": "/api/v1/bikes",
                "methods": ["GET", "POST"]
            },
            "get_bike_by_model": {
                "url": "/api/v1/bikes/model/<model_name>",
                "method": "GET"
            },
            "update_or_delete_bike_by_id": {
                "url": "/api/v1/bikes/id/<bike_id>",
                "methods": ["PUT", "DELETE"]
            }
        }
    })

@app.route('/api/v1/bikes', methods=['GET', 'POST'])
def handle_all_bikes():
    """
    Handles fetching all bikes (GET) and creating a new bike (POST).
    This single function manages two different request methods.
    """
    if request.method == 'GET':
        try:
            all_bikes = list(bikes_collection.find())
            result = [serialize_doc(bike) for bike in all_bikes]
            return jsonify(result), 200
        except Exception as e:
            return jsonify({"error": f"An error occurred: {e}"}), 500

    elif request.method == 'POST':
        try:
            new_bike = request.get_json()
            if not new_bike:
                return jsonify({"error": "No data provided in request body"}), 400
            
            result = bikes_collection.insert_one(new_bike)
            return jsonify({
                "message": "Bike added successfully!",
                "inserted_id": str(result.inserted_id)
            }), 201  # 201 Created
        except Exception as e:
            return jsonify({"error": f"An error occurred: {e}"}), 500


@app.route('/api/v1/bikes/id/<string:bike_id>', methods=['PUT', 'DELETE'])
def handle_bike_by_id(bike_id):
    """
    Handles updating (PUT) and deleting (DELETE) a specific bike by its _id.
    """
    try:
        # Convert the string ID from the URL to a valid MongoDB ObjectId
        obj_id = ObjectId(bike_id)
    except InvalidId:
        return jsonify({"error": "Invalid bike ID format"}), 400

    if request.method == 'PUT':
        try:
            update_data = request.get_json()
            if not update_data:
                return jsonify({"error": "No update data provided"}), 400
            
            result = bikes_collection.update_one({'_id': obj_id}, {'$set': update_data})
            if result.modified_count > 0:
                return jsonify({"message": f"Bike with ID {bike_id} updated successfully!"}), 200
            else:
                return jsonify({"error": f"Bike with ID {bike_id} not found or no new data provided"}), 404
        except Exception as e:
            return jsonify({"error": f"An error occurred: {e}"}), 500

    elif request.method == 'DELETE':
        try:
            result = bikes_collection.delete_one({'_id': obj_id})
            if result.deleted_count > 0:
                return jsonify({"message": f"Bike with ID {bike_id} deleted successfully!"}), 200
            else:
                return jsonify({"error": f"Bike with ID {bike_id} not found"}), 404
        except Exception as e:
            return jsonify({"error": f"An error occurred: {e}"}), 500


@app.route('/api/v1/bikes/model/<string:model>', methods=['GET'])
def handle_bike_by_model(model):
    """Fetches a single bike by its model name (case-insensitive)."""
    try:
        bike = bikes_collection.find_one({"model": {"$regex": f'^{model}$', "$options": "i"}})
        if bike:
            return jsonify(serialize_doc(bike)), 200
        else:
            return jsonify({"error": f"Bike with model '{model}' not found"}), 404
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500


# --- Run the App ---
if __name__ == '__main__':
    # This print statement helps you confirm that you are running the latest version of the code.
    print("--- Flask server is starting with the LATEST app.py code ---")
    app.run(debug=True)

