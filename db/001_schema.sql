CREATE TABLE IF NOT EXISTS people(
person_id BIGSERIAL PRIMARY KEY,
first_name VARCHAR(30) NOT NULL,
last_name VARCHAR(30) NOT NULL,
username VARCHAR(30) UNIQUE NOT NULL,
password_hash TEXT NOT NULL,
active BOOLEAN NOT NULL DEFAULT TRUE,
created_at TIMESTAMPTZ DEFAULT NOW(),
role VARCHAR(15) NOT NULL CHECK (role IN ('employee', 'supervisor', 'admin'))
);

CREATE TABLE IF NOT EXISTS areas(
area_id BIGSERIAL PRIMARY KEY,
area_name VARCHAR(120) NOT NULL,
area_type VARCHAR(30) NOT NULL,
active BOOLEAN NOT NULL DEFAULT TRUE,
created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS tasktype(
tasktype_id BIGSERIAL PRIMARY KEY,
task_name VARCHAR(30) NOT NULL,
active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS task(
task_id BIGSERIAL PRIMARY KEY,

area_id BIGINT REFERENCES areas(area_id) NOT NULL,

tasktype BIGINT REFERENCES tasktype(tasktype_id) NOT NULL,

scheduled_for DATE NOT NULL DEFAULT CURRENT_DATE,

status VARCHAR(15) NOT NULL CHECK (status IN ('unassigned', 'assigned', 'completed', 'postponed')),
prev_status VARCHAR(15) NOT NULL CHECK (prev_status IN ('unassigned', 'assigned', 'completed', 'postponed')),

assigned_to BIGINT REFERENCES people(person_id),
assigned_by BIGINT REFERENCES people(person_id),

completed_by BIGINT REFERENCES people(person_id),
completed_at TIMESTAMPTZ,

notes TEXT,
created_at TIMESTAMPTZ DEFAULT NOW()
);