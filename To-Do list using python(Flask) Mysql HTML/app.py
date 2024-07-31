from flask import Flask, request, jsonify, render_template
from flask_mysqldb import MySQL
import os

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'todo_db'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tasks', methods=['GET', 'POST'])
def manage_tasks():
    if request.method == 'POST':
        task_content = request.json.get('task')
        if task_content:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO tasks (content) VALUES (%s)", (task_content,))
            mysql.connection.commit()
            cur.close()
            return jsonify({"status": "success", "task": task_content}), 201
        return jsonify({"status": "error", "message": "Task is required"}), 400
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tasks")
    tasks = cur.fetchall()
    cur.close()
    tasks_list = [{"id": task[0], "content": task[1]} for task in tasks]
    return jsonify(tasks_list)

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    mysql.connection.commit()
    cur.close()
    if cur.rowcount > 0:
        return jsonify({"status": "success"}), 200
    return jsonify({"status": "error", "message": "Task not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
