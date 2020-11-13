"""
Functions that interface with the database related to plays and searching.
"""

from flask import current_app as app
from flask_mysqldb import MySQL


mysql = MySQL(app)


def fetch_play(game_id, play_id)
    """
    Retrieve play given `game_id` and `play_id`.

    Args:
      game_id : int
        Identifier for each game
      play_id : int
        Identifier for the play in the game

    Returns:
      rv : Tuple
        Tuple is (game_id, play_id, desc, play_type, posteam, posteam_type, yards_gained, 
                  side_of_field, yrdln, qtr, time, wp, down, ydstogo)
    """
    cur = mysql.connection.cursor()
    sql = """SELECT * FROM Play WHERE game_id=%s AND play_id=%s"""
    cur.execute(sql, (game_id, play_id))
    rv = cur.fetchone()
    return rv


def went_for_it(team):
    """
    Find all plays where `team` went for it on 4th Down.

    Args:
      team : str
        The 3 letter identification name for the team
    
    Returns:
      rv : list[tuple]
        Tuple is (game_id, play_id, desc, play_type, posteam, posteam_type, yards_gained, 
                  side_of_field, yrdln, qtr, time, wp, down, ydstogo)
    """
    cur = mysql.connection.cursor()
    sql = """SELECT * FROM Play WHERE posteam="%s" AND down=4 AND (play_type <> "punt" OR "field_goal")"""
    cur.execute(sql, (team,))
    rv = cur.fetchall()
    return rv


def matchups(teamA, teamB):
    """
    Find all matchups between `teamA` and `teamB`.

    Args:
      teamA : str
        The 3 letter identification name for the team
      teamB : str
        The 3 letter identification name for the team

    Returns:
      rv : list[tuple]
        Tuple is (game_date, home_team, away_team, final_home_score, final_away_score)
    """
    cur = mysql.connection.cursor()
    sql = """SELECT * FROM GameFull WHERE (home_team="%s" OR home_team="%s") AND (away_team="%s" OR away_team="%s")"""
    cur.execute(sql, (teamA, teamB, teamA, teamB))
    rv = cur.fetchall()
    return rv


def penalty(player_name):
    """
    Find all times a player was involved in a penalty.

    Args:
      player_name : str
        Name of the player to search for
    
    Returns:
      rv : list[tuple]
        Tuple is ()