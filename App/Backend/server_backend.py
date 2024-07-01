from flask import Flask, request, jsonify, abort
import os
import json

app = Flask(__name__)

# Get the directory of the current script
current_dir = os.path.dirname(__file__)
data_dir = os.path.join(current_dir, "data")

# Ensure data directory exists
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# File paths relative to the current directory
USERS_FILE = os.path.join(data_dir, "users.json")
TABLES_FILE = os.path.join(data_dir, "tables.json")
MESSAGES_FILE = os.path.join(data_dir, "messages.json")


# Helper functions
def read_json(file_path):
    """Read data from a JSON file."""
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            data = json.load(f)
        return data
    else:
        return []


def write_json(data, file_path):
    """Write data to a JSON file."""
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)


def find_user_by_credentials(username, password):
    """Find user by username and password."""
    users = read_json(USERS_FILE)
    for user in users:
        if user["username"] == username and user["password"] == password:
            return user
    return None


# Endpoints
@app.route("/create_table", methods=["POST"])
def create_table():
    data = request.json
    user_id = data.get("user_id")
    table_name = data.get("name")

    # Read existing tables data
    tables = read_json(TABLES_FILE)

    # Generate a new table ID (for example, based on current timestamp)
    table_id = f"table_{len(tables) + 1}"

    # Create new table entry
    new_table = {"id": table_id, "user_id": user_id, "name": table_name, "messages": []}

    # Append new table to tables list
    tables.append(new_table)

    # Write updated tables data back to JSON file
    write_json(tables, TABLES_FILE)

    return jsonify({"message": "Table created successfully", "table": new_table}), 201


@app.route("/get_tables", methods=["GET"])
def get_tables():
    tables = read_json(TABLES_FILE)
    return jsonify(tables), 200


@app.route("/create_user", methods=["POST"])
def create_user():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    # Read existing users data
    users = read_json(USERS_FILE)

    # Check if username already exists
    for user in users:
        if user["username"] == username:
            return jsonify({"error": "Username already exists"}), 400

    # Generate a new user ID (for example, based on current timestamp)
    user_id = f"user_{len(users) + 1}"

    # Create new user entry
    new_user = {"id": user_id, "username": username, "password": password}

    # Append new user to users list
    users.append(new_user)

    # Write updated users data back to JSON file
    write_json(users, USERS_FILE)

    return jsonify({"message": "User created successfully", "user": new_user}), 201


@app.route("/authenticate_user", methods=["POST"])
def authenticate_user():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    user = find_user_by_credentials(username, password)

    if user:
        return jsonify({"message": "Authentication successful", "user": user}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401


@app.route("/send_message/<table_id>", methods=["POST"])
def send_message(table_id):
    data = request.json
    message = data.get("message")

    # Read existing tables data
    tables = read_json(TABLES_FILE)

    # Find the table to send message
    for table in tables:
        if table["id"] == table_id:
            table["messages"].append(message)
            write_json(tables, TABLES_FILE)
            return (
                jsonify({"message": "Message sent successfully", "table_id": table_id}),
                201,
            )

    return jsonify({"error": f"Table {table_id} not found"}), 404


@app.route("/get_messages/<table_id>", methods=["GET"])
def get_messages(table_id):
    # Read existing tables data
    tables = read_json(TABLES_FILE)

    # Find the table to get messages
    for table in tables:
        if table["id"] == table_id:
            return jsonify(table["messages"]), 200

    return jsonify({"error": f"Table {table_id} not found"}), 404


@app.route("/get_user_tables/<user_id>", methods=["GET"])
def get_user_tables(user_id):
    # Read existing tables data
    tables = read_json(TABLES_FILE)

    # Find tables belonging to the user
    user_tables = [table for table in tables if table["user_id"] == user_id]
    return jsonify(user_tables), 200


# Run the Flask application
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
