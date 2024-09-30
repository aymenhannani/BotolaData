# visualization.py

import pandas as pd
import matplotlib.pyplot as plt

def filter_complete_teams(data, all_years):
    """
    Filters teams that have data for all specified years.

    Parameters:
    data (DataFrame): The team data.
    all_years (array-like): List of years.

    Returns:
    DataFrame: Filtered data.
    """
    return data.groupby('Team').filter(lambda x: set(all_years).issubset(set(x['Season'])))

def plot_value_team(data, value, title=" Evolution by Team and Year", complete=False):
    """
    Plots the evolution of a specified value by team and season.

    Parameters:
    data (DataFrame): The team data.
    value (str): The value to plot.
    title (str): The title of the plot.
    complete (bool): Whether to filter teams with complete data.
    """
    # Prepare data for plotting
    team_values = data.groupby(['Team', 'Season'])[value].mean().reset_index()
    all_years = data['Season'].unique()
    team_values = team_values.sort_values('Season', ascending=True)

    if complete:
        team_values = filter_complete_teams(team_values, all_years)

    # Plotting
    plt.figure(figsize=(16, 8))
    for team in team_values['Team'].unique():
        team_data = team_values[team_values['Team'] == team].sort_values('Season')
        plt.plot(team_data['Season'], team_data[value], marker='o', label=team)

    plt.title(value + title)
    plt.xlabel('Year')
    plt.ylabel(value)
    plt.legend(title='Teams', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    plt.show()
