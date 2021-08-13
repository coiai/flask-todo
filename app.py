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
    connect.close()
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
    connect.close()
    return redirect('/tasklist')

@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/tasklist')
def tasklist():
    connect = sqlite3.connect('flasktest.db')
    cursor = connect.cursor()
    cursor.execute("SELECT id, task FROM task")
    task = cursor.fetchall()
    connect.close()
    # taskのままだとリスト型の中にたぷるなので使いづらい
    # そのためリスト型の中に辞書型を持つtask_listを作る！
    task_list = []
    for row in task:
        task_list.append({"id":row[0], "task":row[1]})
    print(task)
    print(task_list)
    return render_template('tasklist.html', html_task = task_list)  

@app.route('/edit/<int:id>')
def edit(id):
    connect = sqlite3.connect('flasktest.db')
    cursor = connect.cursor()
    cursor.execute("SELECT task FROM task WHERE id = ?",
    (id,))
    task = cursor.fetchone()[0]
    connect.close()
    item = {"id":id, "task":task}
    return render_template('edit.html', html_task = item)

@app.route('/edit', methods=["POST"])
def edt_post():
    id = request.form.get('id')
    task = request.form.get('task')
    connect = sqlite3.connect('flasktest.db')
    cursor = connect.cursor()
    cursor.execute("UPDATE task SET task = ? WHERE id = ? ",
    (task, id))
    connect.commit()
    connect.close()
    return redirect('/tasklist')

if __name__  == "__main__":
    app.run(debug=True)