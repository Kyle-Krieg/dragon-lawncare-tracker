BEGIN;


TRUNCATE TABLE task, tasktype, areas, people
RESTART IDENTITY CASCADE;


INSERT INTO people (first_name, last_name, role, username, password_hash) VALUES
('Kyle', 'Kirkpatrick', 'admin', 'kylek', '$2b$12$O7c8q0Q5X8F7J9K0L1M2N3O4P5Q6R7S8T9U0V1W2X3Y4Z5A6B7C8D9E0F1G2H3I4J5K6L7M8N9O0P1Q2R3S4T5U6V7W8X9Y0Z1'),
('John', 'Doe', 'employee', 'johnd', '$2b$12$O7c8q0Q5X8F7J9K0L1M2N3O4P5Q6R7S8T9U0V1W2X3Y4Z5A6B7C8D9E0F1G2H3I4J5K6L7M8N9O0P1Q2R3S4T5U6V7W8X9Y0Z1'),
('Jane', 'Smith', 'supervisor', 'janes', '$2b$12$O7c8q0Q5X8F7J9K0L1M2N3O4P5Q6R7S8T9U0V1W2X3Y4Z5A6B7C8D9E0F1G2H3I4J5K6L7M8N9O0P1Q2R3S4T5U6V7W8X9Y0Z1');


INSERT INTO areas (area_name, area_type) VALUES
('Front Lawn', 'yard'),
('Back Lawn', 'yard'),
('Side Strip', 'yard');


INSERT INTO tasktype (task_name) VALUES
('mowing'),
('edging'),
('trimming');


INSERT INTO task (area_id, tasktype, scheduled_for, status, prev_status) VALUES
(1, 1, CURRENT_DATE, 'unassigned', 'unassigned'),
(2, 2, CURRENT_DATE + INTERVAL '1 day', 'unassigned', 'unassigned'),
(3, 3, CURRENT_DATE + INTERVAL '2 days', 'unassigned', 'unassigned');


COMMIT;