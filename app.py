from dash import Dash, html, dcc, Input, Output
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash_bootstrap_components as dbc
import dash_dangerously_set_inner_html

# Data import
df = pd.read_csv("assets/overview_fr.csv")

# --------------------------------------------------------backend realisateurs----------------------------------------------------
# --------------- filtrage 1er graph ---------------------

# selection des colonnes
overview_fr_selec = df.loc[:, ["tconst", "primaryTitle", "averageRating", "director1", "budget", "revenue"]]
# drop NaN
overview_fr_selec.dropna(inplace=True)
# sort by budget
overview_fr_by_budget = overview_fr_selec.sort_values(by=["budget"], ascending=False, inplace=False)
# je créé un dataframe avec 20 realisateurs ayant eu le plus de budget

overview_fr_by_budget = overview_fr_by_budget.groupby('director1')['budget'].sum().reset_index()
overview_fr_by_budget.sort_values(by=["budget"], ascending=False, inplace=True)
overview_fr_by_budget = overview_fr_by_budget.nlargest(20, 'budget')

# --------------- filtrage 2eme graph ---------------------

# je créé un dataframe avec 20 realisateurs ayant fait le plus de films
director_count = overview_fr_selec.value_counts(['director1']) 
director_count = pd.DataFrame(director_count, columns = ["Quantité"])
director_count_top20 = director_count.nlargest(20, 'Quantité')
director_count_top20 = director_count_top20.rename_axis("Director").reset_index()

# --------------- filtrage 3eme graph ---------------------

# sort by revenue
overview_fr_by_revenue = overview_fr_selec.sort_values(by=["revenue"], ascending=False, inplace=False)
# réalisateurs qui ont rapporté le plus d’argent 
overview_fr_by_revenue = overview_fr_by_revenue.groupby('director1')['revenue'].sum().reset_index()
overview_fr_by_revenue.sort_values(by=["revenue"], ascending=False, inplace=True)
overview_fr_by_revenue = overview_fr_by_revenue.nlargest(20, 'revenue')

# --------------- filtrage 4eme graph ---------------------

# selection des colonnes
overview_fr_selec_with_time = df.loc[:, ["tconst", "primaryTitle", "startYear", "director1", "budget", "revenue"]]
# drop NaN
overview_fr_selec_with_time.dropna(inplace=True)
# sort by revenue
overview_fr_selec_with_time = overview_fr_selec_with_time.sort_values(by=["revenue"], ascending=False, inplace=False)
# je supprime tous les films qui n'ont pas de revenues
overview_fr_selec_with_time=overview_fr_selec_with_time[overview_fr_selec_with_time["revenue"] > 0]
# sort by Years
overview_fr_selec_with_time = overview_fr_selec_with_time.sort_values(by=["startYear"], ascending=True, inplace=False)


# Les 20 realisateurs ayant eu le plus de budget
fig_overview_fr_by_budget = px.bar(overview_fr_by_budget, x='director1', y='budget',
    title="Les 20 realisateurs ayant eu le plus de budget",
    labels={
                     "budget": "Budget en $",
                     "director1": "Realisateurs"
                 },
    color='budget', width=600, height=400)


# Les 20 realisateurs qui réalisé le plus films
fig_director_count_top20 = px.bar(director_count_top20, x='Director', y='Quantité',
    title="Les 20 realisateurs qui réalisé le plus films",
    labels={
                     "Quantité": "Quantité",
                     "Director": "Realisateurs"
                 },
    color='Quantité', width=600, height=400)


# Les 20 réalisateurs qui ont rapporté le plus d’argent 
fig_overview_fr_by_revenue = px.bar(overview_fr_by_revenue, x='director1', y='revenue',
    title="Les 20 réalisateurs qui ont rapporté le plus d’argent ",
    labels={
                     "revenue": "revenue en $",
                     "director1": "Realisateurs"
                 },
    color='revenue', width=600, height=400)


# Les réalisateurs qui ont rapporté le plus d’argent par année 
fig_overview_fr_selec_with_time = px.bar(overview_fr_selec_with_time, x='director1', y='revenue',
    title="Les réalisateurs qui ont rapporté le plus d’argent par année ",
    labels={
                     "revenue": "revenue en $",
                     "director1": "Realisateurs"
                 },
    color='revenue', 
                    animation_frame ="startYear")


# --------------------------------------------------------backend Genres----------------------------------------------------




# --------------------------------------------------------backend durée----------------------------------------------------




# --------------------------------------------------------backend film----------------------------------------------------




# --------------------------------------------------------backend acteurs actrisses----------------------------------------------------


# Initialisation de l'app
app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


index_page = html.Div([
    dbc.Row([

        

            html.Div([
                html.H1('Recommandations'),
                dbc.Button("Films", outline=True, color="primary", href='/page-1', className='btn'),
                dbc.Button('Acteurs & Actrices', outline=True, color="primary", href='/page-2', className='btn'),
                dbc.Button('Réalisateurs', outline=True, color="primary", href='/page-3', className='btn'),
                dbc.Button('Genres', outline=True, color="primary", href='/page-4', className='btn'),
                dbc.Button('Durée', outline=True, color="primary", href='/page-5', className='btn'),
                
            ]),

            html.Div([
                dcc.Dropdown(['LA', 'NYC', 'MTL'], 'LA', id='page-1-dropdown')
            ]),
        
            
    ], className='text-justify')
])   
page_1_layout = html.Div([
    html.H1('Films'),
    html.Div(id='page-1-content'),
    dbc.Button("Films", outline=True, color="primary", href='/page-1', className='btn'),
    dbc.Button('Acteurs & Actrices', outline=True, color="primary", href='/page-2', className='btn'),
    dbc.Button('Réalisateurs', outline=True, color="primary", href='/page-3', className='btn'),
    dbc.Button('Genres', outline=True, color="primary", href='/page-4', className='btn'),
    dbc.Button('Durée', outline=True, color="primary", href='/page-5', className='btn'),
    dbc.Button('Recommandations', outline=True, color="primary", href='/', className='btn')
])

@app.callback(Output('page-1-content', 'children'),
              [Input('page-1-dropdown', 'value')])
def page_1_dropdown(value):
    return f'You have selected {value}'


page_2_layout = html.Div([
    html.H1('Acteurs & Actrices'),
    html.Div(id='page-2-content'),
    dbc.Button("Films", outline=True, color="primary", href='/page-1', className='btn'),
    dbc.Button('Acteurs & Actrices', outline=True, color="primary", href='/page-2', className='btn'),
    dbc.Button('Réalisateurs', outline=True, color="primary", href='/page-3', className='btn'),
    dbc.Button('Genres', outline=True, color="primary", href='/page-4', className='btn'),
    dbc.Button('Durée', outline=True, color="primary", href='/page-5', className='btn'),
    dbc.Button('Recommandations', outline=True, color="primary", href='/', className='btn')
])

@app.callback(Output('page-2-content', 'children'),
              [Input('page-2-radios', 'value')])
def page_2_radios(value):
    return f'You have selected {value}'





page_3_layout = html.Div([
    html.H1('Réalisateurs'),
    html.Div(id='page-3-content'),
    dbc.Button("Films", outline=True, color="primary", href='/page-1', className='btn'),
    dbc.Button('Acteurs & Actrices', outline=True, color="primary", href='/page-2', className='btn'),
    dbc.Button('Réalisateurs', outline=True, color="primary", href='/page-3', className='btn'),
    dbc.Button('Genres', outline=True, color="primary", href='/page-4', className='btn'),
    dbc.Button('Durée', outline=True, color="primary", href='/page-5', className='btn'),
    dbc.Button('Recommandations', outline=True, color="primary", href='/', className='btn'),
    dcc.Graph(
        id='example-graph',
        figure=fig_overview_fr_by_budget
    ),
    dcc.Graph(
        id='example-graph',
        figure=fig_director_count_top20
    ),
    dcc.Graph(
        id='example-graph',
        figure=fig_overview_fr_by_revenue
    ),
    dcc.Graph(
        id='example-graph',
        figure=fig_overview_fr_selec_with_time
    ),

]),








page_4_layout = html.Div([
    html.H1('Genres'),
    html.Div(id='page-4-content'),
    dbc.Button("Films", outline=True, color="primary", href='/page-1', className='btn'),
    dbc.Button('Acteurs & Actrices', outline=True, color="primary", href='/page-2', className='btn'),
    dbc.Button('Réalisateurs', outline=True, color="primary", href='/page-3', className='btn'),
    dbc.Button('Genres', outline=True, color="primary", href='/page-4', className='btn'),
    dbc.Button('Durée', outline=True, color="primary", href='/page-5', className='btn'),
    dbc.Button('Recommandations', outline=True, color="primary", href='/', className='btn')
])

@app.callback(Output('page-4-content', 'children'),
              [Input('page-4-radios', 'value')])
def page_4_radios(value):
    return f'You have selected {value}'


page_5_layout = html.Div([
    html.H1('Durée'),
    html.Div(id='page-5-content'),
    dbc.Button("Films", outline=True, color="primary", href='/page-1', className='btn'),
    dbc.Button('Acteurs & Actrices', outline=True, color="primary", href='/page-2', className='btn'),
    dbc.Button('Réalisateurs', outline=True, color="primary", href='/page-3', className='btn'),
    dbc.Button('Genres', outline=True, color="primary", href='/page-4', className='btn'),
    dbc.Button('Durée', outline=True, color="primary", href='/page-5', className='btn'),
    dbc.Button('Recommandations', outline=True, color="primary", href='/', className='btn')
])

@app.callback(Output('page-5-content', 'children'),
              [Input('page-5-radios', 'value')])
def page_5_radios(value):
    return f'You have selected {value}'


# Update the index
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-1':
        return page_1_layout
    elif pathname == '/page-2':
        return page_2_layout
    elif pathname == '/page-3':
        return page_3_layout
    elif pathname == '/page-4':
        return page_4_layout
    elif pathname == '/page-5':
        return page_5_layout
    else:
        return index_page
    # You could also return a 404 "URL not found" page here

if __name__ == '__main__':
    app.run_server(debug=True)