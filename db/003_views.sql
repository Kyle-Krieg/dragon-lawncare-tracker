CREATE OR REPLACE VIEW task_list AS
SELECT
    t.task_id,
    a.area_name,
    a.area_type,
    tt.task_name,
    t.scheduled_for,
    t.status,
    t.assigned_to AS assigned_to_id,
    COALESCE(CONCAT(p.first_name, ' ', p.last_name), '(unassigned)') AS assigned_to_name,
    t.completed_at,
    t.completed_by AS completed_by_id,
    t.notes,
    t.created_at
FROM task t
JOIN areas a ON t.area_id = a.area_id
JOIN tasktype tt ON t.tasktype_id = tt.tasktype_id
LEFT JOIN people p ON t.assigned_to = p.person_id
WHERE a.active = TRUE
  AND tt.active = TRUE;

CREATE OR REPLACE VIEW due_tasks AS
SELECT *
FROM task_list
WHERE status <> 'completed'
  AND scheduled_for <= CURRENT_DATE
ORDER BY scheduled_for, task_id;

CREATE OR REPLACE VIEW completed_tasks AS
SELECT *
FROM task_list
WHERE status = 'completed'
  AND completed_at IS NOT NULL
ORDER BY completed_at DESC, task_id;

CREATE OR REPLACE VIEW assignable_tasks AS
SELECT *
FROM task_list
WHERE status = 'unassigned'
ORDER BY scheduled_for, task_id;
