import requests
import pandas as pd
import concurrent.futures
import asyncio

def fetch_team_data(team_id, team_name, season, headers):
    """
    Fetches players for a given team in a specific season.
    This function is used in parallel execution.
    """
    players_url = f'https://localhost:8000/clubs/{team_id}/players?season_id={season}'
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

def fetch_team_players_parallel(teams, season, headers):
    """
    Fetches players for all teams in parallel using ThreadPoolExecutor.

    Parameters:
    teams (list): List of team dictionaries containing team_id and team_name.
    season (str): The season year.
    headers (dict): Headers for the HTTP request.

    Returns:
    DataFrame: A DataFrame containing player data for all teams.
    """
    all_players_data = []

    for team in teams :
        team_name = team["name"]
        try:
            team_players_df = fetch_team_data(team["id"],team["name"],season,headers) # This returns the DataFrame from fetch_team_data
            if not team_players_df.empty:
                team_players_df['Team'] = team_name  # Add team name to the DataFrame
                team_players_df['Season'] = season   # Add season to the DataFrame
                all_players_data.append(team_players_df)
        except Exception as e:
            print(f"Error fetching players for {team_name}: {e}")

    # Concatenate all data into a single DataFrame
    if all_players_data:
        return pd.concat(all_players_data, ignore_index=True)
    else:
        return pd.DataFrame()

# Example of calling fetch_competition_teams and fetch_team_players_parallel
def get_all_season_data():
    headers = {'accept': 'application/json'}
    list_seasons = [str(i) for i in range(2015, 2025)]
    all_season_data = pd.DataFrame()

    for season in list_seasons:
        # Fetch the teams for the season
        teams = fetch_competition_teams(season, headers)
        print(teams)

        # Fetch the players in parallel for all teams in the season
        season_data = fetch_team_players_parallel(teams, season, headers)

        # Append the season data to the all_season_data DataFrame
        if not season_data.empty:
            all_season_data = pd.concat([all_season_data, season_data], ignore_index=True)

    return all_season_data
