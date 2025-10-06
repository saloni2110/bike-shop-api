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
    raise ValueError("MONGO_URI is not set in the environment variables")

# Set up the MongoDB Client
client = MongoClient(uri)
db = client.bikedb
bikes_collection = db.bikes

# --- Helper Function for JSON conversion ---
def serialize_doc(doc):
    if doc and "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc

# --- API Routes ---

@app.route('/')
def handle_index():
    # Instead of returning JSON, we now tell Flask to find and return an HTML file.
    return jsonify('index.html')

# If you still want the API welcome message, you can move it to a different route.
# This is a good practice!
@app.route('/api/v1')
def api_welcome():
    return jsonify({
        "message": "Welcome to the Bike Shop API!",
        "api_endpoints": {
            "all_bikes": "/api/v1/bikes",
            "bike_by_model": "/api/v1/bikes/model/<model>",
            "bike_by_id": "/api/v1/bikes/id/<bike_id>"
        }
    })

@app.route('/api/v1/bikes', methods=['GET', 'POST'])
def handle_all_bikes():
    if request.method == 'POST':
        try:
            new_bike = request.get_json()

            # --- NEW VALIDATION LOGIC STARTS HERE ---
            if not new_bike:
                return jsonify({"error": "No data provided in request body"}), 400

            required_fields = ["make", "model", "price", "type"]
            missing_fields = [field for field in required_fields if field not in new_bike]
            if missing_fields:
                return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400

            if not isinstance(new_bike.get("price"), (int, float)):
                return jsonify({"error": "Price must be a number"}), 400
            # --- NEW VALIDATION LOGIC ENDS HERE ---

            result = bikes_collection.insert_one(new_bike)
            return jsonify({
                "message": "Bike added successfully!",
                "inserted_id": str(result.inserted_id)
            }), 201

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    elif request.method == 'GET':
        try:
            all_bikes = list(bikes_collection.find())
            result = [serialize_doc(bike) for bike in all_bikes]
            return jsonify(result), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

@app.route('/api/v1/bikes/model/<string:model>', methods=['GET'])
def handle_bike_by_model(model):
    try:
        bike = bikes_collection.find_one({"model": {"$regex": f'^{model}$', "$options": "i"}})
        if bike:
            return jsonify(serialize_doc(bike)), 200
        else:
            return jsonify({"error": "Bike not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/v1/bikes/id/<string:bike_id>', methods=['PUT', 'DELETE'])
def handle_bike_by_id(bike_id):
    try:
        obj_id = ObjectId(bike_id)
    except InvalidId:
        return jsonify({"error": "Invalid bike ID format"}), 400

    if request.method == 'PUT':
        try:
            update_data = request.get_json()
            if not update_data:
                return jsonify({"error": "No update data provided"}), 400

            result = bikes_collection.update_one(
                {'_id': obj_id},
                {'$set': update_data}
            )
            if result.modified_count > 0:
                return jsonify({"message": f"Bike with ID {bike_id} updated successfully!"}), 200
            else:
                return jsonify({"error": f"Bike with ID {bike_id} not found or no new data provided"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    elif request.method == 'DELETE':
        try:
            result = bikes_collection.delete_one({'_id': obj_id})
            if result.deleted_count > 0:
                return jsonify({"message": f"Bike with ID {bike_id} deleted successfully!"}), 200
            else:
                return jsonify({"error": f"Bike with ID {bike_id} not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500

# --- Run the App ---
if __name__ == '__main__':
    print("--- Flask server is starting with the LATEST app.py code ---")
    app.run(debug=True)

# Note: In a production environment, consider using a WSGI server like Gunicorn to run the app.