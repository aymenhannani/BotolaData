import requests
import pandas as pd
import concurrent.futures
import asyncio

def fetch_team_data(team_id, team_name, season, headers):
    """
    Fetches players for a given team in a specific season.
    This function is used in parallel execution.
    """
    players_url = f'http://localhost:8000/clubs/{team_id}/players?season_id={season}'
    response = requests.get(players_url, headers=headers)
    if response.status_code == 200:
        players_data = response.json().get('players', [])
        return pd.DataFrame(players_data)  # Return DataFrame for consistency
    else:
        print(f"Failed to fetch players for {team_name} in season {season}. Status code: {response.status_code}")
        return pd.DataFrame()
    
    
def fetch_competition_teams(list_seasons, headers):
    """
    Fetches teams for a given competition season.

    Parameters:
    season (str): The season year.
    headers (dict): Headers for the HTTP request.

    Returns:
    list: A list of team dictionaries.
    """
    teams={}
    for season in list_seasons :
        competition_url = f'http://localhost:8000/competitions/MAR1/clubs?season_id={season}'
        
        response = requests.get(competition_url, headers=headers)

        if response.status_code == 200:
            competition_data = response.json()
            teams[season] = competition_data.get('clubs', [])
            print(teams)
        else:
            print(f"Failed to fetch teams for season {season}. Status code: {response.status_code}")
            teams[season] = []


    return teams



def fetch_team_players(teams, season ,headers):
    all_players_data = []
    for team in teams :
        team_name = team["name"]
        team_players_df = fetch_team_data(team["id"],team["name"],season,headers) # This returns the DataFrame from fetch_team_data
    return team_players_df

def fetch_season_data(teams,season,headers):
    dict_season={}   
    df=pd.DataFrame()
    for team in teams :
        dict_season[team["name"]]=fetch_team_data(team["id"],team["name"],season,headers)
        dict_season[team["name"]]["Team"]=team["name"]
    df=pd.concat([ dict_season[teamdf] for teamdf in dict_season])
    return df

def get_all_season_data():
    headers = {'accept': 'application/json'}
    list_seasons = [str(i) for i in range(2015, 2025)]
    season_data={}
    all_season_data = pd.DataFrame()
    teams = fetch_competition_teams(list_seasons, headers)
    for season in list_seasons:
        # Fetch the players in parallel for all teams in the season
        season_data[season] = fetch_team_players_parallel(teams[season], season, headers)

    return season_data

