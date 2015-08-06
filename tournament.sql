-- Table definitions for the tournament project.
CREATE DATABASE tournament;
\c tournament

CREATE TABLE players (
    id SERIAL,
    name TEXT,
    wins INTEGER,
    matches INTEGER
);
