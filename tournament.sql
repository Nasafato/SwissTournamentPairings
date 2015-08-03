-- Table definitions for the tournament project.
CREATE TABLE players (
    id SERIAL,
    name TEXT,
    wins INTEGER,
    matches INTEGER
);

CREATE TABLE matches (
    id SERIAL
    player1_id INTEGER
    player2_id INTEGER
    result INTEGER
);



