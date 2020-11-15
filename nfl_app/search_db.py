"""
Functions that interface with the database related to plays and searching.
"""

from nfl_app.conndb import mysql


def fetch_play(game_id, play_id):
    """
    Retrieve play given `game_id` and `play_id`.

    Args:
      game_id : int
        Identifier for each game
      play_id : int
        Identifier for the play in the game

    Returns:
      rv : tuple[tuple]
        Inner tuple is (game_id, play_id, desc, play_type, posteam, posteam_type, yards_gained,
                  side_of_field, yrdln, qtr, time, wp, down, ydstogo)
    """
    cur = mysql.connection.cursor()
    sql = """SELECT * FROM Play WHERE game_id=%s AND play_id=%s"""
    cur.execute(sql, (game_id, play_id))
    rv = cur.fetchone()
    cur.close()
    return rv


def went_for_it(team):
    """
    Find all plays where `team` went for it on 4th Down.

    Args:
      team : str
        The 3 letter identification name for the team

    Returns:
      rv : tuple[tuple]
        Inner tuple is (game_id, play_id, desc, play_type, posteam, posteam_type, yards_gained,
                  side_of_field, yrdln, qtr, time, wp, down, ydstogo)
    """
    cur = mysql.connection.cursor()
    sql = """SELECT * FROM Play WHERE posteam=%s AND down=4 AND (play_type <> "punt" AND play_type <> "field_goal" AND play_type <> "no_play")"""
    cur.execute(sql, (team,))
    rv = cur.fetchall()
    cur.close()
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
      rv : tuple[tuple]
        Inner tuple is (game_date, home_team, away_team, final_home_score, final_away_score)
    """
    cur = mysql.connection.cursor()
    sql = """SELECT * FROM GameFull WHERE (home_team=%s OR home_team=%s) AND (away_team=%s OR away_team=%s)"""
    cur.execute(sql, (teamA, teamB, teamA, teamB))
    rv = cur.fetchall()
    cur.close()
    return rv


def penalty(player_name):
    """
    Find all times a player was involved in a penalty.

    Args:
      player_name : str
        Name of the player to search for

    Returns:
      rv : tuple[tuple]
        Inner tuple is (game_id, play_id, penalty_team, penalty_player_name, penalty_yards)
    """
    cur = mysql.connection.cursor()
    # player_name = mysql.connection.escape_string(player_name)
    sql = f'SELECT * FROM PenaltyPlay WHERE penalty_player_name LIKE "%{player_name}%"'
    cur.execute(sql)
    rv = cur.fetchall()
    cur.close()
    return rv


def punter(player_name):
    """
    Find all times a certain punter kicked.

    Args:
      player_name : str
        Name of the player to search for

    Returns:
      rv : tuple[tuple]
        Inner tuple is (game_id, play_id, field_goal_result, kick_distance, extra_point_result,
                  kickoff_returned_player_name, return_yards, punter_player_name,
                  kicker_player_name, punt_returner_player_name)
    """
    cur = mysql.connection.cursor()
    # player_name = mysql.connection.escape_string(player_name)
    sql = f'SELECT * FROM KickPlay WHERE punter_player_name LIKE "%{player_name}%"'
    cur.execute(sql)
    rv = cur.fetchall()
    cur.close()
    return rv


def kicker(player_name):
    """
    Find all times a certain kicker kicked.

    Args:
      player_name : str
        Name of the player to search for

    Returns:
      rv : tuple[tuple]
        Inner tuple is (game_id, play_id, field_goal_result, kick_distance, extra_point_result,
                  kickoff_returned_player_name, return_yards, punter_player_name,
                  kicker_player_name, punt_returner_player_name)
    """
    cur = mysql.connection.cursor()
    # player_name = mysql.connection.escape_string(player_name)
    sql = f'SELECT * FROM KickPlay WHERE kicker_player_name LIKE "%{player_name}%"'
    cur.execute(sql)
    rv = cur.fetchall()
    cur.close()
    return rv


def passer(player_name):
    """
    Find all times a certain player passed.

    Args:
      player_name : str
        Name of the player to search for

    Returns:
      rv : tuple[tuple]
        Inner tuple is (game_id, play_id, pass_length, pass_location, air_yards, yards_after_catch,
                  passer_player_name, receiver_player_name, incomplete_pass)
    """
    cur = mysql.connection.cursor()
    # player_name = mysql.connection.escape_string(player_name)
    sql = f'SELECT * FROM PassPlay WHERE passer_player_name LIKE "%{player_name}%"'
    cur.execute(sql)
    rv = cur.fetchall()
    cur.close()
    return rv


def receiver(player_name):
    """
    Find all times a certain player passed.

    Args:
      player_name : str
        Name of the player to search for

    Returns:
      rv : tuple[tuple]
        Inner tuple is (game_id, play_id, pass_length, pass_location, air_yards, yards_after_catch,
                  passer_player_name, receiver_player_name, incomplete_pass)
    """
    cur = mysql.connection.cursor()
    # player_name = mysql.connection.escape_string(player_name)
    sql = f'SELECT * FROM PassPlay WHERE receiver_player_name LIKE "%{player_name}%"'
    cur.execute(sql)
    rv = cur.fetchall()
    cur.close()
    return rv


def rusher(player_name):
    """
    Find all times a certain player rushed.

    Args:
      player_name : str
        Name of the player to search for

    Returns:
      rv : tuple[tuple]
        Inner tuple is (game_id, play_id, run_gap, run_location, rusher_player_name, yards_gained)
    """
    cur = mysql.connection.cursor()
    # player_name = mysql.connection.escape_string(player_name)
    sql = f'SELECT * FROM RunPlay WHERE rusher_player_name LIKE "%{player_name}%"'
    cur.execute(sql)
    rv = cur.fetchall()
    cur.close()
    return rv
