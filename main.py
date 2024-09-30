# main.py

import pandas as pd
from data_extraction import fetch_competition_teams, fetch_team_players
from data_processing import clean_player_data, aggregate_all_data
from visualization import plot_value_team

def main():
    # Initialize variables
    headers = {'accept': 'application/json'}
    list_seasons = [str(i) for i in range(2015, 2025)]
    all_players_data = []

    # Loop through each season
    for season in list_seasons:
        print(f"Processing season: {season}")
        teams = fetch_competition_teams(season, headers)

        # Loop through each team
        for team in teams:
            team_id = team['id']
            team_name = team['name']

            # Fetch and clean player data
            df_players = fetch_team_players(team_id, team_name, season, headers)
            if not df_players.empty:
                df_players = clean_player_data(df_players)
                all_players_data.append(df_players)

    # Aggregate all data
    df_all = aggregate_all_data(all_players_data)

    # Save aggregated data to CSV (optional)
    df_all.to_csv('aggregated_player_data.csv', index=False)

    # Plot the data
    plot_value_team(df_all, value='marketValue', complete=True)

if __name__ == '__main__':
    main()
