from flask import Flask, request, jsonify, make_response, redirect, url_for
from flask.templating import render_template
from flask_cors import CORS
from flask_restful import Api,Resource
from flask_sqlalchemy import SQLAlchemy
import json
import mysql.connector

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False #ให้ผลลัพธ์ไม่ออกมาเป็น Ascii (แสดงภาษาไทยได้)
CORS(app)
host = "localhost"
user = "root"
db = "foodbooked"
password = ""
api=Api(app)


@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route("/api/user")
def read():
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True) #เรียกดูข้อมูลเป็น dictionary
    mycursor.execute("SELECT * FROM user")
    myresults = mycursor.fetchall()
    return make_response(jsonify(myresults), 200)

@app.route("/api/user/<id>")
def readbyid(id):
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)
    sql = "SELECT * FROM user WHERE ID = %s"
    val = (id,) #id คือค่าที่รับมาจาก parameter / ใส่ , เพื่อบ่งบอกว่าอันนี้(id)คือคู่อันดับ
    mycursor.execute(sql, val) # %s from sql = id from val
    myresults = mycursor.fetchall()
    return make_response(jsonify(myresults), 200)

@app.route("/api/user", methods = ['POST'])
def create():
    data = request.get_json() #create column
    # ตรวจสอบว่าข้อมูลไม่เป็นค่าว่าง
    if not data['Username'] or not data['Email'] or not data['Password']:
        return make_response(jsonify({"error": "กรุณากรอกข้อมูลให้ครบถ้วน"}), 400)
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)
    sql = "INSERT INTO user (Username, Email, Password) VALUES (%s, %s, %s)"
    val = (data['Username'], data['Email'], data['Password'])
    mycursor.execute(sql, val)
    mydb.commit()
    return make_response(jsonify({ "rowcount": mycursor.rowcount }), 200) #บอกว่ามีการแก้ไขกี่ row

@app.route("/api/user/<id>", methods = ['PUT'])
def update(id):
    data = request.get_json()
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)
    sql = "UPDATE user SET Username = %s, Email = %s, Password = %s WHERE id = %s"
    val = (data['Username'], data['Email'], data['Password'], id)
    mycursor.execute(sql, val)
    mydb.commit()
    return make_response(jsonify({ "rowcount": mycursor.rowcount }), 200)

@app.route("/api/user/<id>", methods = ['DELETE'])
def delete(id):
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)
    sql = "DELETE FROM user WHERE id = %s"
    val = (id,)
    mycursor.execute(sql, val)
    mydb.commit()
    return make_response(jsonify({ "rowcount": mycursor.rowcount }), 200)


@app.route('/table-data')
def data():
    mydb = 'test'
    return render_template('table-data.html', mydb)


if __name__ == "__main__":
    app.run(debug=True)
