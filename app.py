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
