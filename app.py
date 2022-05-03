from dash import Dash, html, dcc, Input, Output
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import dash_dangerously_set_inner_html

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
    dbc.Button('Recommandations', outline=True, color="primary", href='/', className='btn')
])

@app.callback(Output('page-3-content', 'children'),
              [Input('page-3-radios', 'value')])
def page_3_radios(value):
    return f'You have selected {value}'


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