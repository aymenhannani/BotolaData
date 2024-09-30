# data_extraction.py

import requests
import pandas as pd

def fetch_competition_teams(season, headers):
    """
    Fetches teams for a given competition season.

    Parameters:
    season (str): The season year.
    headers (dict): Headers for the HTTP request.

    Returns:
    list: A list of team dictionaries.
    """
    competition_url = 'http://localhost:8000/competitions/MAR1/clubs?season_id=' + season
    response = requests.get(competition_url, headers=headers)

    if response.status_code == 200:
        competition_data = response.json()
        teams = competition_data.get('clubs', [])
    else:
        print(f"Failed to fetch teams for season {season}. Status code: {response.status_code}")
        teams = []

    return teams

def fetch_team_players(team_id, team_name, season, headers):
    """
    Fetches players for a given team and season.

    Parameters:
    team_id (int): The team's ID.
    team_name (str): The team's name.
    season (str): The season year.
    headers (dict): Headers for the HTTP request.

    Returns:
    DataFrame: A DataFrame containing player data.
    """
    players_url = f'http://localhost:8000/clubs/{team_id}/players?season_id={season}'
    response = requests.get(players_url, headers=headers)

    if response.status_code == 200:
        players_data = response.json()
        df_players = pd.DataFrame(players_data.get('players', []))
        df_players['Team'] = team_name
        df_players['Season'] = season
        return df_players
    else:
        print(f"Failed to fetch players for {team_name} in season {season}. Status code: {response.status_code}")
        return pd.DataFrame()
