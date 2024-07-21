from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import json
import mysql.connector

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)
host = "localhost"
user = "root"
password = ""
db = "users"

@app.route("/api/users")
def read():
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("SELECT * FROM users")
    myresult = mycursor.fetchall()
    return make_response(jsonify(myresult), 200)

@app.route("/api/users/<uid>")
def readbyid(uid):
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)
    sql = "SELECT * FROM users WHERE uid = %s"
    val = (uid,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    return make_response(jsonify(myresult), 200)

@app.route("/api/users/new", methods = ['POST'])
def new():
    data = request.get_json()
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)
    sql = "INSERT INTO users (uid, name, age) VALUES (%s, %s, %s)"
    val = (data['uid'], data['name'], data['age'])
    mycursor.execute(sql, val)
    mydb.commit()
    return make_response(jsonify({"rowcount":mycursor.rowcount}), 200)

@app.route("/api/users/<uid>", methods = ['PUT'])
def update(uid):
    data = request.get_json()
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)
    sql = "UPDATE users SET name = %s, age = %s WHERE uid =%s"
    val = (data['name'], data['age'], uid)
    mycursor.execute(sql, val)
    mydb.commit()
    return make_response(jsonify({"rowcount":mycursor.rowcount}), 200)

@app.route("/api/users/<uid>", methods = ['DELETE'])
def delete(uid):
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)
    sql = "DELETE FROM users WHERE uid = %s"
    val = (uid,)
    mycursor.execute(sql, val)
    mydb.commit()
    return make_response(jsonify({"rowcount":mycursor.rowcount}), 200)