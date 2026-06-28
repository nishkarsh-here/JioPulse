-- JioPulse database schema
-- Paste this whole file into Supabase: SQL Editor -> New query -> Run.

create table if not exists teachers (
  teacher_id bigint generated always as identity primary key,
  username text unique not null,
  password text not null,
  name text not null,
  created_at timestamptz default now()
);

create table if not exists students (
  student_id bigint generated always as identity primary key,
  name text not null,
  face_embedding jsonb,
  voice_embedding jsonb,
  created_at timestamptz default now()
);

create table if not exists subjects (
  subject_id bigint generated always as identity primary key,
  subject_code text not null,
  name text not null,
  section text,
  teacher_id bigint references teachers(teacher_id) on delete cascade,
  created_at timestamptz default now()
);

create table if not exists subject_students (
  id bigint generated always as identity primary key,
  student_id bigint references students(student_id) on delete cascade,
  subject_id bigint references subjects(subject_id) on delete cascade
);

create table if not exists attendance_logs (
  id bigint generated always as identity primary key,
  student_id bigint references students(student_id) on delete cascade,
  subject_id bigint references subjects(subject_id) on delete cascade,
  "timestamp" text,
  is_present boolean default false,
  created_at timestamptz default now()
);

-- This app reads/writes with the project key directly (no Supabase Auth),
-- so disable row-level security on these tables.
alter table teachers          disable row level security;
alter table students          disable row level security;
alter table subjects          disable row level security;
alter table subject_students  disable row level security;
alter table attendance_logs   disable row level security;
