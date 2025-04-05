from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import pymysql
import bcrypt  # Import bcrypt for password hashing
from backend.config import Config
  
auth_bp = Blueprint("auth", __name__)

# Connect to MySQL
def get_db_connection():
    return pymysql.connect(host=Config.MYSQL_HOST, user=Config.MYSQL_USER,
                           password=Config.MYSQL_PASSWORD, db=Config.MYSQL_DB)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    try:
        # Hash the password and decode to UTF-8 string
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        connection = get_db_connection()
        cursor = connection.cursor()

        # Insert the user into the database, using the decoded hashed password
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, hashed_password))
        connection.commit()

        cursor.close()
        connection.close()
        return jsonify({"message": "User registered successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        connection.close()

        if user:
            # Assuming user columns: 0:id, 1:username, 2:full_name, 3:email, 4:password_hash, 5:role, etc.
            stored_hash = user[2]  # password_hash should be at index 4
            # Compare provided password with stored hash (convert stored_hash to bytes)
            if bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8")):
                token = create_access_token(identity=username)
                return jsonify({"access_token": token})
            else:
                return jsonify({"error": "Invalid credentials"}), 401
        else:
            return jsonify({"error": "User not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    username = get_jwt_identity()
    return jsonify({"message": f"Welcome {username}!"})

