

from flask import Blueprint, jsonify, request, render_template

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")

@auth_bp.route("/register", methods=["GET"])
def register_page():
    return render_template("register.html")



@auth_bp.route("/api/auth/login", methods=["POST"])
def login():


    data = request.get_json()

    #Call users database to verify that login credentials are correct


    return jsonify({"message": "Login successful"}), 200



@auth_bp.route("/api/auth/register", methods=["POST"])
def register():
    data = request.get_json()
    

    #Call users database to verify not already registered, then inserts new user


    return jsonify({"message": "User registered"}), 201



@auth_bp.route("/api/auth/logout", methods=["POST"])
def logout():
    return jsonify({"message": "Logged out"}), 200