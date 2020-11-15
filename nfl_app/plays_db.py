"""
Functions that edit the play table for admin actions
"""


from nfl_app.conndb import mysql


def edit_play(play_data):
    """
    takes a dictionary of following format and edits the play in the database
        fields = {
        "new_game_id": "",
        "new_play_id": "",
        "new_desc": "",
        "new_play_type": "",
        "new_posteam": "",
        "new_posteam_type": "",
        "new_yards_gained": "",
        "new_side_of_field": "",
        "new_yrdln": "",
        "new_qtr": "",
        "new_time": "",
        "new_wp": "",
        "new_down": "",
        "new_ydstogo": ""
    }
    """
    keys = ["new_game_id", "new_play_id", "new_desc", "new_play_type","new_posteam","new_posteam_type","new_yards_gained","new_side_of_field","new_yrdln","new_qtr","new_time","new_wp","new_down","new_ydstogo", "old_game_id", "old_play_id"]
    play_data["old_game_id"] = play_data["new_game_id"]
    play_data["old_play_id"] = play_data["new_play_id"]
    cur = mysql.connection.cursor()
    sql = """UPDATE `Play` SET `game_id`=%s,`play_id`=%s, `desc`=%s,`play_type`=%s, `posteam`=%s, `posteam_type`=%s, yards_gained=%s, side_of_field=%s, yrdln=%s, qtr=%s, time=%s, wp=%s, down=%s, ydstogo=%s WHERE game_id=%s AND play_id=%s;"""
    cur.execute(sql, (play_data[key] for key in keys))
    mysql.connection.commit()
    cur.close()


def add_play(play_type, play_data):
    """
    takes a dictionary of following format and adds the play to the play table
        fields = {
        "game_id": "",
        "play_id": "",
        "desc": "",
        "play_type": "",
        "posteam": "",
        "posteam_type": "",
        "yards_gained": "",
        "side_of_field": "",
        "yrdln": "",
        "qtr": "",
        "time": "",
        "wp": "",
        "down": "",
        "ydstogo": ""
    }
    """
    keys = ["game_id", "play_id", "desc", "play_type","posteam","posteam_type","yards_gained","side_of_field","yrdln","qtr","time","wp","down","ydstogo"]
    cur = mysql.connection.cursor()
    sql = "INSERT INTO Play VALUES ("
    for field in keys:
        sql += "'" + play_data[key] + "', "
    sql = sql[:-2] + ");"
    cur.execute(sql, (play_data[key] for key in keys))
    mysql.connection.commit()
    cur.close()


def delete_play(game_id, play_id):
    """
    delete play with game id and play id
    """
    sql = """DELETE FROM `Play` WHERE `game_id`=%s,`play_id`=%s;"""
    cur = mysql.connection.cursor()
    cur.execute(sql, (game_id, play_id,))
    mysql.connection.commit()
    cur.close()