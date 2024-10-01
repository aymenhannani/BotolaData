# app.py

import dash
from dash import dcc, html, callback, Output, Input
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from data_extraction import fetch_competition_teams, fetch_team_players
from data_processing import clean_player_data, aggregate_all_data

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Team Market Value Dashboard"
server = app.server  # Required for deployment later

# Track the number of API requests
api_request_counter = 0

# Fetch and process data (you can refactor this into functions or modules as needed)
def get_data():
    global api_request_counter
    headers = {'accept': 'application/json'}
    list_seasons = [str(i) for i in range(2015, 2025)]
    all_players_data = []

    for season in list_seasons:
        teams = fetch_competition_teams(season, headers)
        api_request_counter += 1  # Count API request for teams
        for team in teams:
            team_id = team['id']
            team_name = team['name']
            df_players = fetch_team_players(team_id, team_name, season, headers)
            api_request_counter += 1  # Count API request for players
            if not df_players.empty:
                df_players = clean_player_data(df_players)
                all_players_data.append(df_players)
    df_all = aggregate_all_data(all_players_data)
    return df_all

# Fetch the data once when the app starts
df_all = get_data()

# Function to display API request information
def get_api_info():
    return f"Total API Requests: {api_request_counter}"

# Define the layout of the app, including the navigation bar
app.layout = dbc.Container([
    dcc.Location(id='url', refresh=False),  # This will track the URL of the app

    # Navigation Bar
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dcc.Link('Home', href='/', className="nav-link")),
            dbc.NavItem(dcc.Link('Developer Page', href='/developer', className="nav-link"))
        ],
        brand="Team Market Value Dashboard",
        color="primary",
        dark=True,
        className="mb-4"
    ),

    # Content of the page will be inserted here
    html.Div(id='page-content', className="mt-4")
], fluid=True)


# Main page layout: Team Market Value Evolution
def market_value_page():
    return dbc.Container([
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


# Developer page layout: Display API request information
def developer_page():
    return dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Developer Page"), className="mb-2")
        ]),
        dbc.Row([
            dbc.Col(html.P("This page shows information about the API requests made to Transfermarkt."))
        ]),
        dbc.Row([
            dbc.Col(html.Div(id='api-info'))
        ])
    ], fluid=True)


# Routing: Display the correct page based on the URL
@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/developer':
        return developer_page()
    else:
        return market_value_page()


# Callback to update the graph on the main page
@app.callback(
    Output('value-graph', 'figure'),
    [Input('team-dropdown', 'value')]
)
def update_graph(selected_teams):
    filtered_data = df_all[df_all['Team'].isin(selected_teams)]
    team_values = filtered_data.groupby(['Team', 'Season'])['marketValue'].mean().reset_index()
    fig = px.line(team_values, x='Season', y='marketValue', color='Team', markers=True)
    fig.update_layout(title='Market Value Evolution by Team and Season')
    return fig


# Callback to update the API information on the developer page
@app.callback(
    Output('api-info', 'children'),
    [Input('url', 'pathname')]
)
def update_api_info(pathname):
    if pathname == '/developer':
        return get_api_info()
    return ""


if __name__ == '__main__':
    app.run_server(debug=True)
