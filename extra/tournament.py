#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament_ec")


def deleteAllMatches():
    """Remove all the match records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM matches;")
    c.execute("UPDATE join_player_tournament SET wins = 0, matches = 0;") 
    DB.commit()
    DB.close()

def deleteMatchesFromTournament(name):
    DB = connect()
    c = DB.cursor()
    c.execute('''
              DELETE
              FROM matches 
              WHERE tournament_id IN
              (SELECT id FROM tournaments
              WHERE tournament_name = (%s));
              ''', (name,))
    c.execute('''
              UPDATE join_player_tournament
              SET wins = 0, matches = 0, points = 0
              FROM tournaments
              WHERE join_player_tournament.tournament_id = tournaments.id;
              ''')
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

def registerTournament(name):
    """Adds a tournament to the tournament database.

    The database assigns a unique serial id number for the player.
    """
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT * FROM tournaments WHERE tournament_name = (%s);", (name,))
    
    matching_tournaments = c.fetchall()
    if len(matching_tournaments) > 0:
        DB.commit()
        DB.close()
        print("\tERROR: tournament name already exists - please choose another name")
        return False
    
    c.execute("INSERT INTO tournaments (tournament_name) VALUES (%s);", (name,))

    DB.commit()
    DB.close()
    return True

def deleteTournament(name):

    """Deletes a tournament from the tournaments table"""
    DB = connect()
    c = DB.cursor()
    c.execute('''DELETE FROM join_player_tournament USING tournaments
              WHERE join_player_tournament.tournament_id = tournaments.id
              AND tournaments.tournament_name = (%s);''', (name,))
    c.execute("DELETE FROM tournaments WHERE tournament_name = (%s);", (name,))
    DB.commit()
    DB.close()

def registerPlayer(name):
    """Adds a player to the database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    DB = connect()
    c = DB.cursor()
    c.execute("INSERT INTO players (name) VALUES (%s);", (name,))
    DB.commit()
    DB.close()

def lookupTournamentKey(tournament_name):
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT * FROM tournaments WHERE tournament_name = (%s);", (tournament_name,))
    data = c.fetchall()
    DB.close()

    return data

def lookupPlayerKey(player_name):
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT * FROM players WHERE name = (%s);", (player_name,))
    data = c.fetchall()
    DB.close()

    return data

def registerPlayerForTournament(tournament_id, player_id):
    DB = connect()
    c = DB.cursor()
    c.execute('''
              INSERT INTO join_player_tournament (tournament_id, player_id)
              VALUES (%s, %s);
              ''', (tournament_id, player_id))
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
    c.execute("SELECT * FROM players ORDER BY wins DESC;")
    player_list = c.fetchall()
    DB.close()
    return player_list


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.
    Updates the point values of the players who have played against winner and won

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect()
    c = DB.cursor()


    # Updating the winner's point total
    c.execute("SELECT points FROM players WHERE id = (%s);", (winner,))
    p1_oldpoints = c.fetchone()[0]
    c.execute("SELECT points FROM players WHERE id = (%s);", (loser,))
    p2_points = c.fetchone()[0]
    p1_points = p1_oldpoints + p2_points
    
    c.execute("UPDATE players SET wins = wins+1, matches = matches+1, points = (%s) WHERE id = (%s);", (p1_points, winner))
    c.execute("UPDATE players SET matches = matches+1 WHERE id = (%s);", (loser,))

    # Update the points of those who have won against the winner

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
    
    pre_pairings = zip(player_list[::2], player_list[1::2])
    for tup in pre_pairings:
        pairings.append(tup[0]+tup[1])
    
    return pairings

def oddPairings():
    """Like swissPairings(), except in the case of odd numbers of players,
    gives the odd one out a bye."""

    
