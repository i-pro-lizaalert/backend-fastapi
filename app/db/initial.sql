create table if not exists users
(
	id serial primary key,
	username text not null unique,
	hashed_password text not null,
	name text not null,
	surname text not null,
	avatar text
);