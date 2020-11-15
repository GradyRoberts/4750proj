"""
Handle search
"""
from nfl_app.search_db import (
    went_for_it,
    matchups,
    passer,
    receiver,
    rusher,
    punter,
    kicker,
    penalty,
)


def perform_search(form):
    rows = None
    search_type = form.get("form_name")
    template = ""
    if search_type == "wentforit":
        rows = went_for_it(form.get("team_name"))
        template = "res_play.html"
    elif search_type == "matchup":
        rows = matchups(form.get("teamA"), form.get("teamB"))
        template = "res_game.html"
    elif search_type == "penalty":
        rows = penalty(form.get("player_name"))
        template = "res_penalty.html"
    elif search_type == "punter":
        rows = punter(form.get("player_name"))
        template = "res_kick.html"
    elif search_type == "kicker":
        rows = kicker(form.get("player_name"))
        template = "res_kick.html"
    elif search_type == "passer":
        rows = passer(form.get("player_name"))
        template = "res_pass.html"
    elif search_type == "receiver":
        rows = receiver(form.get("player_name"))
        template = "res_pass.html"
    elif search_type == "rusher":
        rows = rusher(form.get("player_name"))
        template = "res_run.html"
    return rows, template
