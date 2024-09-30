# app.py

import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
from data_extraction import fetch_competition_teams, fetch_team_players
from data_processing import clean_player_data, aggregate_all_data
import plotly.express as px

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Fetch and process data (you can refactor this into functions or modules as needed)
def get_data():
    headers = {'accept': 'application/json'}
    list_seasons = [str(i) for i in range(2015, 2025)]
    all_players_data = []

    for season in list_seasons:
        teams = fetch_competition_teams(season, headers)
        for team in teams:
            team_id = team['id']
            team_name = team['name']
            df_players = fetch_team_players(team_id, team_name, season, headers)
            if not df_players.empty:
                df_players = clean_player_data(df_players)
                all_players_data.append(df_players)
    df_all = aggregate_all_data(all_players_data)
    return df_all

df_all = get_data()

# Layout of the app
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Team Market Value Evolution"), className="mb-2")
    ]),
    dbc.Row([
        dbc.Col(
            dcc.Dropdown(
                id='team-dropdown',
                options=[{'label': team, 'value': team} for team in sorted(df_all['Team'].unique())],
                value=df_all['Team'].unique().tolist(),
                multi=True
            ), width=12
        )
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='value-graph'), width=12)
    ])
], fluid=True)

# Callback to update the graph based on selected teams
@app.callback(
    dash.dependencies.Output('value-graph', 'figure'),
    [dash.dependencies.Input('team-dropdown', 'value')]
)
def update_graph(selected_teams):
    filtered_data = df_all[df_all['Team'].isin(selected_teams)]
    team_values = filtered_data.groupby(['Team', 'Season'])['marketValue'].mean().reset_index()
    fig = px.line(team_values, x='Season', y='marketValue', color='Team', markers=True)
    fig.update_layout(title='Market Value Evolution by Team and Season')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
