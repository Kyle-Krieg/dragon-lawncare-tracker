from flask import Flask, jsonify, render_template
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


# -----------------------------
# Basic page routes
# These serve the HTML templates
# for the different user roles.
# -----------------------------
@app.get("/")
def home():
    return render_template("index.html")

@app.get("/employee")
def employee_page():
    return render_template("employee.html")

@app.get("/supervisor")
def supervisor_page():
    return render_template("supervisor.html")

@app.get("/supervisor/assign")
def supervisor_assign_page():
    return render_template("supervisor_assign.html")

@app.get("/supervisor/tasks")
def supervisor_tasks_page():
    return render_template("supervisor_tasks.html")

@app.get("/admin")
def admin_page():
    return render_template("admin.html")

@app.get("/admin/assign")
def admin_assign_page():
    return render_template("admin_assign.html")

@app.get("/admin/reopen")
def admin_reopen_page():
    return render_template("admin_reopen.html")

@app.get("/admin/reports")
def admin_reports_page():
    return render_template("admin_reports.html")


# -----------------------------
# Task endpoints
# These return task data with area,
# assignment, and completion details.
# -----------------------------
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
            cur.execute(
                """
                SELECT *
                FROM task_list
                WHERE task_id = %s
                """,
                (task_id,)
            )
            task = cur.fetchone()

    if task:
        return jsonify(task)
    else:
        return jsonify({"error": "Task not found"}), 404


# Marks a task as completed.
# The completed_by field is set to the current assignee.
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
                (task_id,)
            )
            updated_task = cur.fetchone()
        conn.commit()

    if updated_task:
        return jsonify(updated_task)
    else:
        return jsonify({"error": "Task not found"}), 404


# Returns active, non-completed tasks assigned to a specific person.
# This route works for both employees and supervisors.
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


# Assigns a task to a specific person and marks it as assigned.
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
                (employee_id, task_id)
            )
            updated_task = cur.fetchone()
        conn.commit()

    if updated_task:
        return jsonify(updated_task)
    else:
        return jsonify({"error": "Task not found"}), 404


# Removes a current task assignment and returns it to unassigned.
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
                (task_id,)
            )
            updated_task = cur.fetchone()
        conn.commit()

    if updated_task:
        return jsonify(updated_task)
    else:
        return jsonify({"error": "Task not found"}), 404


# Reopens a completed task.
# For V1, reopened tasks always return to unassigned
# so they can be reviewed and reassigned manually.
@app.post("/tasks/<int:task_id>/reopen")
def reopen_task(task_id):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE task
                SET status = 'unassigned',
                    assigned_to = NULL,
                    completed_at = NULL,
                    completed_by = NULL
                WHERE task_id = %s
                  AND status = 'completed'
                RETURNING *;
                """,
                (task_id,)
            )
            updated_task = cur.fetchone()
        conn.commit()

    if updated_task:
        return jsonify(updated_task)
    else:
        return jsonify({"error": "Task not found"}), 404


# -----------------------------
# Reporting endpoints
# These return completed tasks for
# daily, weekly, monthly, and yearly views.
# -----------------------------
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
                """
            )
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
                """
            )
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
                """
            )
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
                """
            )
            tasks = cur.fetchall()
    return jsonify(tasks)


# -----------------------------
# People and assignment endpoints
# These return active users and
# tasks that are available to assign.
# -----------------------------
@app.get("/people")
def get_people():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT person_id, first_name, last_name, role
                FROM people
                WHERE active = TRUE
                ORDER BY last_name, first_name;
                """
            )
            people = cur.fetchall()
    return jsonify(people)

@app.get("/assignable_tasks")
def get_assignable_tasks():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT *
                FROM assignable_tasks
                ORDER BY scheduled_for, task_id;
                """
            )
            tasks = cur.fetchall()
    return jsonify(tasks)


if __name__ == "__main__":
    app.run(debug=True)