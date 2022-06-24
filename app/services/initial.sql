create extension if not exists "uuid-ossp";
create table if not exists users
(
	id serial primary key,
	username text not null unique,
	hashed_password text not null,
	name text not null,
	surname text not null,
	avatar text
);
create table if not exists cases
(
    id uuid primary key,
    name text not null
);
create table if not exists files
(
    source text primary key,
    description text,
    date timestamp
);
create table if not exists tags
(
    id serial primary key,
    name text not null unique
);
create table if not exists files_cases
(
    file_id text references files(source) on delete cascade,
    case_id uuid references cases(id) on delete cascade
);
create table if not exists files_tags
(
    file_id text references files(source) on delete cascade,
    tag_id integer references tags(id) on delete cascade
);
create table if not exists users_cases
(
    user_id integer references users(id) on delete cascade,
    case_id uuid references cases(id) on delete cascade
);