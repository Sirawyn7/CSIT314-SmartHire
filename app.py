
"""
Handles setup of flask server
Calls setup of database
"""

from flask import Flask, jsonify
from database import DatabaseManager
from routes import blueprints



#Server setup
app = Flask(
    __name__,
    template_folder="web/templates",
    static_folder="web/static"
)


db = DatabaseManager("parking.db")

#Registration of routes
for blueprint in blueprints:
    app.register_blueprint(blueprint)



#Placeholder code for server testing
#Run server and access http://127.0.0.1:5000/ping to verify server is online
@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"message": "Server is running"}), 200


if __name__ == "__main__":
    #Server startup
    app.run(debug=True)