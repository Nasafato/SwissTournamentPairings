#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("UPDATE players SET wins = 0, matches = 0;") 
    DB.commit()
    DB.close()


def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM players;")
    DB.commit()
    DB.close()


def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    c = DB.cursor()	
    c.execute("SELECT count(*) FROM players;")
    num_players = c.fetchall()
    DB.close()
    return int(num_players[0][0])
    

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    DB = connect()
    c = DB.cursor()
    c.execute("INSERT INTO players (name, wins, matches) VALUES (%s, 0, 0);", (name,))
    DB.commit()
    DB.close()



def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT * FROM players ORDER BY wins desc;")
    player_list = c.fetchall()
    DB.close()
    return player_list


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect()
    c = DB.cursor()
    # Increments the number of wins of the winner by 1, as well as the number of matches he/she has played by 1
    # Increments the nubmer of matches the loser has played by 1
    c.execute("UPDATE players SET wins = wins+1, matches = matches+1 WHERE id = (%s);", (winner,))
    c.execute("UPDATE players SET matches = matches+1 WHERE id = (%s);", (loser,))
    DB.commit()
    DB.close()

 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT id, name FROM players ORDER BY wins DESC, id;")
    player_list = c.fetchall()
    DB.close()

    pairings = []
    
    # Creates a list of tuples, each tuple being a pair of players, for the next round of the tournament
    pre_pairings = zip(player_list[::2], player_list[1::2])
    for tup in pre_pairings:
        pairings.append(tup[0]+tup[1])
    
    return pairings


