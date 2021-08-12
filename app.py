from flask import Flask, render_template, request, redirect
import sqlite3
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/hello')
def hello():
    return "はじめてのFlaskデビュー🐥"

@app.route('/greet/<text>')
def greet(text):
    return text + "さんこんにちは"

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/info')
def info():
    name = "coiai"
    age = 21
    address = "香川県"
    return render_template('info.html',
     html_name = name,
     html_age = age,
     html_address = address)

@app.route('/weather')
def weather():
    today_weather =  "雨"
    return render_template('weather.html', html_weather = today_weather)

@app.route('/dbtest')
def dbtest():
    # データベースに接続
    connect = sqlite3.connect('flasktest.db')
    cursor = connect.cursor()
    # データベースに命令
    cursor.execute("SELECT name, age, address FROM user WHERE id=1")
    user_info = cursor.fetchone()
    cursor.close()
    print(user_info)
    return render_template('dbtest.html',html_info = user_info)

@app.route('/add', methods=["POST"])
def add_post():
    py_task = request.form.get("html_task")
    connect = sqlite3.connect('flasktest.db')
    cursor = connect.cursor()
    cursor.execute("INSERT INTO task VALUES(null, ?)",(py_task,))
    # DB を保存
    connect.commit()
    cursor.close()
    return redirect('/weather')

@app.route('/add')
def add():
    return render_template('add.html')

if __name__  == "__main__":
    app.run(debug=True)