
from flask import Flask, jsonify
import os

import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

def get_conn():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise RuntimeError("DATABASE_URL environment variable not set")
    return psycopg.connect(db_url, row_factory=dict_row)

@app.get("/")
def home():
    return {"status": "lawncare backend is running"}

@app.get("/tasks")
def get_tasks():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM task_list ORDER BY task_id")
            tasks = cur.fetchall()
    return jsonify(tasks)

@app.get("/tasks/<int:task_id>")
def get_task(task_id):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                        SELECT * 
                        FROM task_list 
                        WHERE task_id = %s
                        """,
                        (task_id,))
            task = cur.fetchone()
    if task:
        return jsonify(task)
    else:
        return jsonify({"error": "Task not found"}), 404

@app.post("/tasks/<int:task_id>/complete")
def complete_task(task_id):  
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                        """
                        UPDATE task
                        SET status = 'completed',
                        completed_at = NOW(),
                        completed_by = assigned_to
                        WHERE task_id = %s 
                        RETURNING *;
                        """, 
                        (task_id,))
            updated_task = cur.fetchone()
    if updated_task:
        return jsonify(updated_task)
    else:
        return jsonify({"error": "Task not found"}), 404

@app.post("/tasks/<int:task_id>/assign")
def assign_task(task_id):   
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                        """
                        UPDATE task
                        SET status = 'assigned'
                        WHERE task_id = %s 
                        RETURNING *;
                        """, 
                        (task_id,))
            updated_task = cur.fetchone()
    if updated_task:
        return jsonify(updated_task)
    else:
        return jsonify({"error": "Task not found"}), 404
