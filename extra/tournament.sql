-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

--CREATE TABLE posts ( content TEXT,
--                     time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--                     id SERIAL );

CREATE DATABASE tournament_ec;
\c tournament_ec;

CREATE TABLE players (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE tournaments (
    id SERIAL PRIMARY KEY,
    tournament_name TEXT,
    winner_id INTEGER REFERENCES players (id)
);

CREATE TABLE matches (
    id SERIAL PRIMARY KEY,
    player1_id INTEGER REFERENCES players (id),
    player2_id INTEGER REFERENCES players (id),
    result INTEGER,
    tournament_id INTEGER REFERENCES tournaments (id)
);

CREATE TABLE join_player_tournament (
    id SERIAL PRIMARY KEY,
    tournament_id INTEGER REFERENCES tournaments (id),
    player_id INTEGER REFERENCES players (id),
    wins INTEGER,
    matches INTEGER,
    points INTEGER,
    has_bye_left BOOLEAN
);

