from flask import Flask, request
import json
from markupsafe import escape
from flask_jwt_extended import JWTManager, jwt_required
from controller.utlisateur_controller import UtilisateurController

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "Une phrase secrète d'une complexité à couper le souffle !"
jwt = JWTManager(app)

@app.route("/user/create", methods=["POST"])
@jwt_required()
def createUser():
    user = UtilisateurController()
    body = request.get_json()
    user.addUser(
        escape(body["email"]),
        escape(body["pseudo"]),
        escape(body["password"]),
        escape(body["role"])
    )
    response = {
        "result": "success"
    }
    return json.dumps(response, separators=(",",":"))

@app.route("/user/<id>/delete", methods=["DELETE"])
@jwt_required()
def deleteUser(id):
    user = UtilisateurController()
    user.deleteUser(int(escape(id)))
    response = {
        "result": "success"
    }
    return json.dumps(response, separators=(",",":"))

@app.route("/user/<id>", methods=["GET"])
@jwt_required()
def getUser(id):
    user = UtilisateurController()
    response = user.getUser(int(escape(id)))
    return json.dumps(response, separators=(",",":"))

@app.route("/user/<id>/update", methods=["PUT"])
@jwt_required()
def updateUser(id):
    user = UtilisateurController()
    body = request.get_json()
    user.updateUser(escape(id),body)
    response = {
        "result": "success"
    }
    return json.dumps(response, separators=(",",":"))

@app.route("/login", methods=["POST"])
def login():
    user = UtilisateurController()
    body = request.get_json()
    token = user.login(body)
    response = {
        "access_token": token
    }
    return json.dumps(response, separators=(",",":"))