
BEGIN;


TRUNCATE TABLE task, tasktype, areas, people
RESTART IDENTITY CASCADE;


INSERT INTO people (first_name, last_name, role) VALUES
('Kyle', 'Kirkpatrick', 'admin'),
('John', 'Doe', 'employee'),
('Jane', 'Smith', 'supervisor'),
('Emily', 'Johnson', 'employee'),
('Michael', 'Brown', 'employee'),
('Sarah', 'Davis', 'supervisor');


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


INSERT INTO task (area_id, tasktype, scheduled_for, status) VALUES
(1, 1, CURRENT_DATE, 'unassigned'),
(2, 2, CURRENT_DATE + INTERVAL '1 day', 'unassigned'),
(3, 3, CURRENT_DATE + INTERVAL '2 days', 'unassigned'),
(4, 4, CURRENT_DATE + INTERVAL '3 days', 'unassigned'),
(5, 5, CURRENT_DATE + INTERVAL '4 days', 'unassigned'),
(6, 6, CURRENT_DATE + INTERVAL '5 days', 'unassigned'),
(7, 7, CURRENT_DATE + INTERVAL '6 days', 'unassigned'),
(8, 8, CURRENT_DATE + INTERVAL '7 days', 'unassigned'),
(9, 1, CURRENT_DATE + INTERVAL '8 days', 'unassigned'),
(10, 2, CURRENT_DATE + INTERVAL '9 days', 'unassigned'),
(11, 3, CURRENT_DATE + INTERVAL '10 days', 'unassigned'),
(12, 4, CURRENT_DATE + INTERVAL '11 days', 'unassigned'),
(13, 5, CURRENT_DATE + INTERVAL '12 days', 'unassigned'),
(14, 6, CURRENT_DATE + INTERVAL '13 days', 'unassigned'),
(15, 7, CURRENT_DATE + INTERVAL '14 days', 'unassigned');


COMMIT;