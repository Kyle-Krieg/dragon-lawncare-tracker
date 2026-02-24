
BEGIN;


TRUNCATE TABLE task, tasktype, areas, people
RESTART IDENTITY CASCADE;


INSERT INTO people (first_name, last_name, role, username, password_hash) VALUES
('Kyle', 'Kirkpatrick', 'admin', 'kylek', '$2b$12$O7c8q0Q5X8F7J9K0L1M2N3O4P5Q6R7S8T9U0V1W2X3Y4Z5A6B7C8D9E0F1G2H3I4J5K6L7M8N9O0P1Q2R3S4T5U6V7W8X9Y0Z1'),
('John', 'Doe', 'employee', 'johnd', '$2b$12$O7c8q0Q5X8F7J9K0L1M2N3O4P5Q6R7S8T9U0V1W2X3Y4Z5A6B7C8D9E0F1G2H3I4J5K6L7M8N9O0P1Q2R3S4T5U6V7W8X9Y0Z1'),
('Jane', 'Smith', 'supervisor', 'janes', '$2b$12$O7c8q0Q5X8F7J9K0L1M2N3O4P5Q6R7S8T9U0V1W2X3Y4Z5A6B7C8D9E0F1G2H3I4J5K6L7M8N9O0P1Q2R3S4T5U6V7W8X9Y0Z1'),
('Emily', 'Johnson', 'employee', 'emilyj', '$2b$12$O7c8q0Q5X8F7J9K0L1M2N3O4P5Q6R7S8T9U0V1W2X3Y4Z5A6B7C8D9E0F1G2H3I4J5K6L7M8N9O0P1Q2R3S4T5U6V7W8X9Y0Z1'),
('Michael', 'Brown', 'employee', 'michaelb', '$2b$12$O7c8q0Q5X8F7J9K0L1M2N3O4P5Q6R7S8T9U0V1W2X3Y4Z5A6B7C8D9E0F1G2H3I4J5K6L7M8N9O0P1Q2R3S4T5U6V7W8X9Y0Z1'),
('Sarah', 'Davis', 'supervisor', 'sarahd', '$2b$12$O7c8q0Q5X8F7J9K0L1M2N3O4P5Q6R7S8T9U0V1W2X3Y4Z5A6B7C8D9E0F1G2H3I4J5K6L7M8N9O0P1Q2R3S4T5U6V7W8X9Y0Z1');


INSERT INTO areas (area_name, area_type) VALUES
('Front Lawn', 'yard'),
('Back Lawn', 'yard'),
('Side Strip', 'yard'),
('Upper School', 'courtyard'),
('Lower School', 'courtyard'),
('Upper School flower bed - front left', 'flower bed'),
('Upper School flower bed - front right', 'flower bed'),
('Upper School flower bed - gym entrance', 'flower bed'),
('Upper School flower bed - behind gym', 'flower bed'),
('Lower School pick-up zone', 'roadway'),
('Lower School parking lot', 'parking lot'),
('Lower School pick-up flower bed - left', 'flower bed'),
('Lower School pick-up flower bed - right', 'flower bed'),
('Middle school flower bed - left', 'flower bed'),
('Middle school flower bed - right', 'flower bed');


INSERT INTO tasktype (task_name) VALUES
('mowing'),
('edging'),
('trimming'),
('weed spraying'),
('mulching'),
('leaf blowing'),
('snow removal'),
('general cleanup');


INSERT INTO task (area_id, tasktype, scheduled_for, status, prev_status) VALUES
(1, 1, CURRENT_DATE, 'unassigned', 'unassigned'),
(2, 2, CURRENT_DATE + INTERVAL '1 day', 'unassigned', 'unassigned'),
(3, 3, CURRENT_DATE + INTERVAL '2 days', 'unassigned', 'unassigned'),
(4, 4, CURRENT_DATE + INTERVAL '3 days', 'unassigned', 'unassigned'),
(5, 5, CURRENT_DATE + INTERVAL '4 days', 'unassigned', 'unassigned'),
(6, 6, CURRENT_DATE + INTERVAL '5 days', 'unassigned', 'unassigned'),
(7, 7, CURRENT_DATE + INTERVAL '6 days', 'unassigned', 'unassigned'),
(8, 8, CURRENT_DATE + INTERVAL '7 days', 'unassigned', 'unassigned'),
(9, 1, CURRENT_DATE + INTERVAL '8 days', 'unassigned', 'unassigned'),
(10, 2, CURRENT_DATE + INTERVAL '9 days', 'unassigned', 'unassigned'),
(11, 3, CURRENT_DATE + INTERVAL '10 days', 'unassigned', 'unassigned'),
(12, 4, CURRENT_DATE + INTERVAL '11 days', 'unassigned', 'unassigned'),
(13, 5, CURRENT_DATE + INTERVAL '12 days', 'unassigned', 'unassigned'),
(14, 6, CURRENT_DATE + INTERVAL '13 days', 'unassigned', 'unassigned'),
(15, 7, CURRENT_DATE + INTERVAL '14 days', 'unassigned', 'unassigned');


COMMIT;