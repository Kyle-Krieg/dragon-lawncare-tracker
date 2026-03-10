
from flask import Flask, jsonify, render_template
import os

import datetime

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

# Basic routes to serve the HTML templates for the different user roles
@app.get("/")
def home():
    return render_template("index.html")

@app.get("/employee")
def employee_page():
    return render_template("employee.html")

@app.get("/supervisor")
def supervisor_page():
    return render_template("supervisor.html")

@app.get("/admin")
def admin_page():
    return render_template("admin.html")

# Endpoint to retrieve all tasks with area and assignment information
@app.get("/tasks")
def get_tasks():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM task_list ORDER BY task_id")
            tasks = cur.fetchall()
    return jsonify(tasks)

# Endpoint to get a specific task by ID, including details about the assigned employee and completion information if applicable
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
    
# Endpoint to mark a task as completed. This will update the task's status to 'completed',
# set the completed_at timestamp, and record which employee completed the task based on the assigned_to field
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

# Endpoint to get all tasks assigned to a specific employee
@app.get("/employees/<int:employee_id>/tasks")
def get_employee_tasks(employee_id):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT *
                FROM task_list
                WHERE assigned_to_id = %s
                  AND status <> 'completed'
                ORDER BY scheduled_for, task_id;
                """,
                (employee_id,)
            )
            tasks = cur.fetchall()
    return jsonify(tasks)

# Endpoint to assign a task to an employee
# This will update the task's status to 'assigned' and set the assigned_to field to the specified employee ID
@app.post("/employees/<int:employee_id>/tasks/<int:task_id>/assign")
def assign_task(employee_id, task_id):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                        """
                        UPDATE task
                        SET status = 'assigned',
                        assigned_to = %s
                        WHERE task_id = %s 
                        RETURNING *;
                        """, 
                        (employee_id, task_id))
            updated_task = cur.fetchone()
    if updated_task:
        return jsonify(updated_task)
    else:
        return jsonify({"error": "Task not found"}), 404

# Endpoint to unassign a task from an employee
# This will update the task's status to 'unassigned' and set the assigned_to field to NULL
@app.post("/tasks/<int:task_id>/unassign")
def unassign_task(task_id):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                        """
                        UPDATE task
                        SET status = 'unassigned',
                        assigned_to = NULL
                        WHERE task_id = %s 
                        RETURNING *;
                        """, 
                        (task_id,))
            updated_task = cur.fetchone()
    if updated_task:
        return jsonify(updated_task)
    else:
        return jsonify({"error": "Task not found"}), 404
    
# Admin endpoint to reopen completed tasks in case of mistakes or changes in circumstances
# Reopened tasks will be set to 'assigned' if they were previously assigned, or 'unassigned' if they were not
@app.post("/tasks/<int:task_id>/reopen")
def reopen_task(task_id):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                        """
                        UPDATE task
                        SET status = CASE
                        WHEN assigned_to IS NULL THEN 'unassigned'
                        ELSE 'assigned'
                        END,
                        completed_at = NULL,
                        completed_by = NULL
                        WHERE task_id = %s
                        AND status = 'completed'
                        RETURNING *;
                        """, 
                        (task_id,))
            updated_task = cur.fetchone()
    if updated_task:
        return jsonify(updated_task)
    else:
        return jsonify({"error": "Task not found"}), 404
    
# Reporting endpoints to get completed tasks for different time periods    
@app.get("/completed/today")
def get_completed_today():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                        """
                        SELECT * 
                        FROM task_list 
                        WHERE status = 'completed' 
                        AND completed_at::date = CURRENT_DATE
                        ORDER BY completed_at DESC;
                        """)
            tasks = cur.fetchall()
    return jsonify(tasks)

@app.get("/completed/this_week")
def get_completed_this_week():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                        """
                        SELECT * 
                        FROM task_list 
                        WHERE status = 'completed'
                        AND completed_at >= date_trunc('week', now())
                        ORDER BY completed_at DESC;
                        """)
            tasks = cur.fetchall()
    return jsonify(tasks)

@app.get("/completed/this_month")
def get_completed_this_month():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                        """
                        SELECT * 
                        FROM task_list 
                        WHERE status = 'completed'
                        AND completed_at >= date_trunc('month', now())
                        ORDER BY completed_at DESC;
                        """)
            tasks = cur.fetchall()
    return jsonify(tasks)

@app.get("/completed/this_season")
def get_completed_this_season():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                        """
                        SELECT * 
                        FROM task_list 
                        WHERE status = 'completed'
                        AND completed_at >= date_trunc('year', now())
                        ORDER BY completed_at DESC;
                        """)
            tasks = cur.fetchall()
    return jsonify(tasks)

@app.get("/people")
def get_people():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT person_id, first_name, last_name, role
                FROM people
                WHERE active = TRUE
                ORDER BY last_name, first_name;
            """)
            people = cur.fetchall()
    return jsonify(people)

@app.get("/assignable_tasks")
def get_assignable_tasks():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT *
                FROM assignable_tasks
                ORDER BY scheduled_for, task_id;
            """)
            tasks = cur.fetchall()
    return jsonify(tasks)