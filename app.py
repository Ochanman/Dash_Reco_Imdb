from dash import Dash, html, dcc, Input, Output
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash_bootstrap_components as dbc
import dash_dangerously_set_inner_html
from plotly.subplots import make_subplots
from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


# Data import
df = pd.read_csv("assets/overview_fr.csv")
df_6000 = pd.read_csv("assets/df_6000.csv")
df_ml = df_6000
# transformation des NaN en str vides ""
df_ml = df_ml.replace(np.nan, '', regex=True)
df_6000 = df_ml

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

# subplots avec les 3 graphs
fig_subplots_realisateurs = make_subplots(
    rows=1, cols=3,
    subplot_titles=("Les 20 realisateurs ayant eu le plus de budget", "Les 20 realisateurs qui réalisé le plus films", "Les 20 réalisateurs qui ont rapporté le plus d’argent"))

fig_subplots_realisateurs.add_trace(go.Bar(x=overview_fr_by_budget["director1"], y=overview_fr_by_budget["budget"]),
              row=1, col=1)

fig_subplots_realisateurs.add_trace(go.Bar(x=director_count_top20["Director"], y=director_count_top20["Quantité"]),
              row=1, col=2)

fig_subplots_realisateurs.add_trace(go.Bar(x=overview_fr_by_revenue["director1"], y=overview_fr_by_revenue["revenue"]),
              row=1, col=3)

fig_subplots_realisateurs.update_layout(height=300, width=1500, showlegend=False)




# Les réalisateurs qui ont rapporté le plus d’argent par année 
fig_overview_fr_selec_with_time = px.bar(overview_fr_selec_with_time, x='director1', y='revenue',
    title="Les réalisateurs qui ont rapporté le plus d’argent par année ",
    labels={
                     "revenue": "revenue en $",
                     "director1": "Realisateurs"
                 },
    color='revenue', 
                    animation_frame ="startYear")

fig_subplots_realisateurs.update_layout(height=300, width=1500, showlegend=False)


# --------------------------------------------------------backend Genres----------------------------------------------------
df_genre = df.drop(df[df['startYear'] < 1910].index)

genre1 = df_genre[['startYear','genre1', 'origin_country']]
genre1.rename(columns={'genre1':'genre'}, inplace=True)
genre1['multiple'] = 'main'

genre2 = df_genre[['startYear','genre2', 'origin_country']]
genre2.rename(columns={'genre2':'genre'}, inplace=True)
genre2['multiple'] = 'second'

genre3 = df_genre[['startYear','genre3', 'origin_country']]
genre3.rename(columns={'genre3':'genre'}, inplace=True)
genre3['multiple'] = 'third'

genres= pd.concat([genre1, genre2, genre3])
genres.dropna(subset=['genre'], inplace=True)

#graph des genres produits en fonctions des années
fig_genre_year = px.histogram(genres, x='startYear', color='genre')

fig_genre_year.update_layout(height=350, width=1500)

#graph des nbs de genre
fig_nb_genre = px.histogram(genres, x='genre', color='multiple').update_xaxes(categoryorder="total descending")

fig_nb_genre.update_layout(height=350, width=1500)


# --------------------------------------------------------backend durée----------------------------------------------------
# --------------- filtrage 1er graph ---------------------
## 1 -Graphe Scatter - Evolution de la durée des films : 

# Supprimer les films dont l'année est inférieure à 1910
time_mean1 = df.drop(df[df['startYear'] < 1910].index)
time_mean1

# Faire un tableau avec groupby sur startYear et mean sur runtime
year_runtime = pd.DataFrame(time_mean1.groupby(by = ["startYear"])["runtimeMinutes"].mean())

# Tranformer index "Genres" en colonne : 
year_runtime = year_runtime.rename_axis("startYear").reset_index()



# --------------- filtrage 2ème graph ---------------------
time_mean_before = time_mean1[time_mean1["startYear"] < 1960]
time_mean_after = time_mean1[time_mean1["startYear"] > 1960]
data = {"Minutes":[88,97]}
Comparaison_year = pd.DataFrame.from_dict(data, orient ="index", 
                                          columns = ["Before 1960","After 1960"])



# --------------- filtrage 3ème graph ---------------------
## 3 - Moyenne des notes en fonction de la durée

# Avant tout supprimer les valeurs < 57 minute et supérieur à 133 minutes 
time_mean1 = time_mean1.drop(
                         time_mean1[time_mean1["runtimeMinutes"]
                         < 57.5].index | time_mean1[time_mean1["runtimeMinutes"]
> 133.5].index )

# Faire un tableau avec groupby sur startYear et mean sur runtime
Rating_runtime = pd.DataFrame(time_mean1.groupby(by = ["runtimeMinutes"])["averageRating"].mean())

# Tranformer index "Genres" en colonne : 
Rating_runtime = Rating_runtime.rename_axis("runtimeMinutes").reset_index()



# --------------- filtrage 4ème graph ---------------------
## 4 - Nombre de vote en fonction de la durée 

# Faire un tableau avec groupeby sur startYear et mean sur runtime
Vote_runtime = pd.DataFrame(time_mean1.groupby(by = ["runtimeMinutes"])["numVotes"].mean())

# Tranformer index "Genres" en colonne : 
Vote_runtime = Vote_runtime.rename_axis("runtimeMinutes").reset_index()

# graphs
fig_subplots_Duree = make_subplots(
    rows=2, cols=2,
    subplot_titles=("Evolution de la durée des films", 
                    "Comparaison de la durée des films avant 1960 et après 1960", 
                    "Moyenne des notes en fonction de la durée",
                    "Nombre de vote en fonction de la durée"))

fig_subplots_Duree.add_trace(go.Scatter(x= year_runtime["startYear"], y= year_runtime["runtimeMinutes"]),
              row=1, col=1)
fig_subplots_Duree.update_traces(marker = dict(color='gold'))


fig_subplots_Duree.add_trace(go.Bar(x=["Avant 1960","Après 1960"], y=[88,97]),
              row=1, col=2)


fig_subplots_Duree.add_trace(go.Line(x=Rating_runtime["runtimeMinutes"], y=Rating_runtime["averageRating"]),
              row=2, col=1)


fig_subplots_Duree.add_trace(go.Line(x=Vote_runtime["runtimeMinutes"], y=Vote_runtime["numVotes"]),
              row=2, col=2)


fig_subplots_Duree.update_layout(height=650, width=1200, showlegend=False)



# --------------------------------------------------------backend film----------------------------------------------------
dff = df.loc[:, ["budget", "revenue", "startYear", "genre1"]]
# drop NaN
dff.dropna(inplace=True)
dff = dff[ dff['startYear']!=0 ]

fig_rev_budg = px.scatter(dff, x='budget', y= 'revenue', color='genre1', width=1200, height=300)


dffg = dff.groupby(['startYear', 'genre1']).agg({'budget': ['sum', 'mean'], 'revenue': ['sum', 'mean'] })
dffg.columns = ['budget_sum','budget_mean', 'revenue_sum','revenue_mean']
dffg.reset_index(inplace=True)


fig_budg = px.line(dffg, x= 'startYear',y='budget_sum', color='genre1', width=1200, height=250)



fig_rev = px.line(dffg, x= 'startYear', y='revenue_sum',color='genre1', width=1200, height=250)




# --------------------------------------------------------backend acteurs actrisses----------------------------------------------------

#----------------------------------filtrage graph1----------------------------------
#DataFrame Actresses
actress_distribution = pd.DataFrame(np.concatenate((df["actress1"],
                            df["actress2"],df["actress3"],
                           df["actress4"],df["actress5"]),axis=0)).value_counts()
actress_distribution


actress_distribution = pd.DataFrame(actress_distribution).rename_axis("0").reset_index()
actress_distribution
actress_distribution.columns= ["Actress","films_played"]
actress_distribution


#----------------------------------filtrage graph2----------------------------------

#DataFrame Actors
actor_distribution = pd.DataFrame
actor_distribution = pd.DataFrame(np.concatenate((df["actor1"],
                            ["actor2"],df["actor3"],
                            df["actor4"],df["actor5"]),axis=0)).value_counts()
actor_distribution
actor_distribution= pd.DataFrame(actor_distribution).rename_axis("0").reset_index()
actor_distribution
#DataFrame Actors
actor_distribution.columns = ["Actor","films_played"]

#graph1 Top 10 actices---------------------------------------------------------------

w=actress_distribution.head(10)
fig_top_actress = px.bar(w,x="Actress",
            y="films_played",
            title='Top 10 des actrices populaires',
            opacity=1,
            width=1200, height=400)

fig_top_actress.update_traces(textfont_size=10,
                  marker=dict(color='#CB4154',
                  line=dict(color='#000000', 
                  width=4)))



#graph1 Top 10 acteurs-------------------------------------------------------------

w=actor_distribution.head(10)
fig_top_actor = px.bar(w,x="Actor",
             y="films_played",
            title='Reccurent actors-Top 10',
            labels = {'op 10 des actrices populaires'},
            width=1200, height=400)
            

fig_top_actor.update_traces(textfont_size=10,
                  marker=dict(color='royalblue', line=dict(color='#000000', width=4)))




# Initialisation de l'app
app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


index_page = html.Div([
    dbc.Row([


            html.Div([
                html.Div([
                html.Img(src='assets\img\logo.png', className='img-fluid position-absolute top-0 start-0 imgLogo'),
                ], className='logo col-2'),
                html.Div([
                html.Span('A', style={'color': 'red'}),
                html.Span('ccueil'),], className='h1'),
                dbc.Button('Accueil', outline=True, color="primary", href='/', className='btn btn-outline-primary'),
                dbc.Button("Industrie", outline=True, color="primary", href='/page-1', className='btn btn-outline-primary'),
                dbc.Button('Acteurs & Actrices', outline=True, color="primary", href='/page-2', className='btn btn-outline-primary'),
                dbc.Button('Réalisateurs', outline=True, color="primary", href='/page-3', className='btn btn-outline-primary'),
                dbc.Button('Genres', outline=True, color="primary", href='/page-4', className='btn btn-outline-primary'),
                dbc.Button('Durée', outline=True, color="primary", href='/page-5', className='btn btn-outline-primary'),
                dbc.Button('Recommandations KNN', outline=True, color="primary", href='/page-6', className='btn btn-outline-primary'),
                dbc.Button('Recommandations Cosine', outline=True, color="primary", href='/page-7', className='btn btn-outline-primary'),
                
            ]),

             html.Div([
                 html.Span('Les Vac’', className='h3'),
                 html.Span('Cinés!', className='h3', style={'color': 'red'}), 
                 html.P('Vous vous êtes déjà demandé quoi regarder? Heureusement, il existe un service qui peut vous aider à faire le tri entre tous les contenus qui vous sont proposés et qui vous aidera à trouver les films qui correspondent à vos critères. Vous pouvez faire des recherches précises en insérant des mots-clés, des noms de films. Ce service vous est proposé par Gilles, Leila, David, Olivier et Romain', className='col-6 offset-6'),
                 ], className='baner text-white w-100 position-absolute bottom-0 end-0 text-end pe-2'
            ),
        
            
    ], className='text-justify')
])   




page_1_layout = html.Div([
    html.Div([
                html.Img(src='assets\img\logo.png', className='img-fluid position-absolute top-0 start-0 imgLogo'),
                ], className='logo col-2'),
    html.Div([
    html.Div([
                html.Span('I', style={'color': 'red'}),
                html.Span('ndustrie'),], className='h1'),
    ]),
    html.Div([
    html.Div(id='page-1-content'),
    dbc.Button('Accueil', outline=True, color="primary", href='/', className='btn btn-outline-primary'),
    dbc.Button("Industrie", outline=True, color="primary", href='/page-1', className='btn btn-outline-primary'),
    dbc.Button('Acteurs & Actrices', outline=True, color="primary", href='/page-2', className='btn btn-outline-primary'),
    dbc.Button('Réalisateurs', outline=True, color="primary", href='/page-3', className='btn btn-outline-primary'),
    dbc.Button('Genres', outline=True, color="primary", href='/page-4', className='btn btn-outline-primary'),
    dbc.Button('Durée', outline=True, color="primary", href='/page-5', className='btn btn-outline-primary'),
    dbc.Button('Recommandations KNN', outline=True, color="primary", href='/page-6', className='btn btn-outline-primary'),
    dbc.Button('Recommandations Cosine', outline=True, color="primary", href='/page-7', className='btn btn-outline-primary'),
    ], className='nav'),
    html.Div([
        dcc.Graph(
        id='rev_budg',
        figure=fig_rev_budg
    ),
    dcc.Graph(
        id='budg',
        figure=fig_budg
    ),
      dcc.Graph(
        id='rev',
        figure=fig_rev
    ),
])
]),

@app.callback(Output('page-1-content', 'children'),
              [Input('page-1-dropdown', 'value')])
def page_1_dropdown(value):
    return f'You have selected {value}'


page_2_layout = html.Div([
    html.Div([
                html.Img(src='assets\img\logo.png', className='img-fluid position-absolute top-0 start-0 imgLogo'),
                ], className='logo col-2'),
    html.Div([
    html.Div([
                html.Span('A', style={'color': 'red'}),
                html.Span('cteurs & '),
                html.Span('A', style={'color': 'red'}),
                html.Span('ctrices'),], className='h1'),
    ]),
    html.Div([
    html.Div(id='page-2-content'),
    dbc.Button('Accueil', outline=True, color="primary", href='/', className='btn btn-outline-primary'),
    dbc.Button("Industrie", outline=True, color="primary", href='/page-1', className='btn btn-outline-primary'),
    dbc.Button('Acteurs & Actrices', outline=True, color="primary", href='/page-2', className='btn btn-outline-primary'),
    dbc.Button('Réalisateurs', outline=True, color="primary", href='/page-3', className='btn btn-outline-primary'),
    dbc.Button('Genres', outline=True, color="primary", href='/page-4', className='btn btn-outline-primary'),
    dbc.Button('Durée', outline=True, color="primary", href='/page-5', className='btn btn-outline-primary'),
    dbc.Button('Recommandations KNN', outline=True, color="primary", href='/page-6', className='btn btn-outline-primary'),
    dbc.Button('Recommandations Cosine', outline=True, color="primary", href='/page-7', className='btn btn-outline-primary'),
    ], className='nav'),
    html.Div([
        dcc.Graph(id='top_actress',
            figure=fig_top_actress
            ),
        dcc.Graph(id='top_actor',
            figure=fig_top_actor
        ),

     ]),
]),

@app.callback(Output('page-2-content', 'children'),
              [Input('page-2-radios', 'value')])
def page_2_radios(value):
    return f'You have selected {value}'





page_3_layout = html.Div([
    html.Div([
                html.Img(src='assets\img\logo.png', className='img-fluid position-absolute top-0 start-0 imgLogo'),
                ], className='logo col-2'),
    html.Div([
    html.Div([
                html.Span('R', style={'color': 'red'}),
                html.Span('éalisateur'),], className='h1'),
    ]),
    html.Div([
    html.Div(id='page-3-content'),
    dbc.Button('Accueil', outline=True, color="primary", href='/', className='btn btn-outline-primary'),
    dbc.Button("Industrie", outline=True, color="primary", href='/page-1', className='btn btn-outline-primary'),
    dbc.Button('Acteurs & Actrices', outline=True, color="primary", href='/page-2', className='btn btn-outline-primary'),
    dbc.Button('Réalisateurs', outline=True, color="primary", href='/page-3', className='btn btn-outline-primary'),
    dbc.Button('Genres', outline=True, color="primary", href='/page-4', className='btn btn-outline-primary'),
    dbc.Button('Durée', outline=True, color="primary", href='/page-5', className='btn btn-outline-primary'),
    dbc.Button('Recommandations KNN', outline=True, color="primary", href='/page-6', className='btn btn-outline-primary'),
    dbc.Button('Recommandations Cosine', outline=True, color="primary", href='/page-7', className='btn btn-outline-primary'),
    ], className='nav'),
html.Div([
    dcc.Graph(
        id='subplots_realisateurs',
        figure=fig_subplots_realisateurs
    ),
    dcc.Graph(
        id='overview_fr_selec_with_time',
        figure=fig_overview_fr_selec_with_time
    ),
]),
]),








page_4_layout = html.Div([
    html.Div([
                html.Img(src='assets\img\logo.png', className='img-fluid position-absolute top-0 start-0 imgLogo'),
                ], className='logo col-2'),
    html.Div([
    html.Div([
                html.Span('G', style={'color': 'red'}),
                html.Span('enres'),], className='h1'),
    ]),
    html.Div([
    html.Div(id='page-4-content'),
    dbc.Button('Accueil', outline=True, color="primary", href='/', className='btn btn-outline-primary'),
    dbc.Button("Industrie", outline=True, color="primary", href='/page-1', className='btn btn-outline-primary'),
    dbc.Button('Acteurs & Actrices', outline=True, color="primary", href='/page-2', className='btn btn-outline-primary'),
    dbc.Button('Réalisateurs', outline=True, color="primary", href='/page-3', className='btn btn-outline-primary'),
    dbc.Button('Genres', outline=True, color="primary", href='/page-4', className='btn btn-outline-primary'),
    dbc.Button('Durée', outline=True, color="primary", href='/page-5', className='btn btn-outline-primary'),
    dbc.Button('Recommandations KNN', outline=True, color="primary", href='/page-6', className='btn btn-outline-primary'),
    dbc.Button('Recommandations Cosine', outline=True, color="primary", href='/page-7', className='btn btn-outline-primary'),
    ], className='nav'),
html.Div([
    dcc.Graph(
        id='genre_year',
        figure=fig_genre_year
    ),
    dcc.Graph(
        id='nb_genre',
        figure=fig_nb_genre
    ),
]),
]),


@app.callback(Output('page-4-content', 'children'),
              [Input('page-4-radios', 'value')])
def page_4_radios(value):
    return f'You have selected {value}'


page_5_layout = html.Div([
    html.Div([
                html.Img(src='assets\img\logo.png', className='img-fluid position-absolute top-0 start-0 imgLogo'),
                ], className='logo col-2'),
    html.Div([
    html.Div([
                html.Span('D', style={'color': 'red'}),
                html.Span('urée'),], className='h1'),
    ]),
    html.Div([
    html.Div(id='page-5-content'),
    dbc.Button('Accueil', outline=True, color="primary", href='/', className='btn btn-outline-primary'),
    dbc.Button("Industrie", outline=True, color="primary", href='/page-1', className='btn btn-outline-primary'),
    dbc.Button('Acteurs & Actrices', outline=True, color="primary", href='/page-2', className='btn btn-outline-primary'),
    dbc.Button('Réalisateurs', outline=True, color="primary", href='/page-3', className='btn btn-outline-primary'),
    dbc.Button('Genres', outline=True, color="primary", href='/page-4', className='btn btn-outline-primary'),
    dbc.Button('Durée', outline=True, color="primary", href='/page-5', className='btn btn-outline-primary'),
    dbc.Button('Recommandations KNN', outline=True, color="primary", href='/page-6', className='btn btn-outline-primary'),
    dbc.Button('Recommandations Cosine', outline=True, color="primary", href='/page-7', className='btn btn-outline-primary'),
    ], className='nav'),
html.Div([
    dcc.Graph(id="subplots_Duree",
           figure = fig_subplots_Duree),

]),
]),


@app.callback(Output('page-5-content', 'children'),
              [Input('page-5-radios', 'value')])
def page_5_radios(value):
    return f'You have selected {value}'



page_6_layout = html.Div([
    dbc.Row([


            html.Div([
                html.Div([
                html.Img(src='assets\img\logo.png', className='img-fluid position-absolute top-0 start-0 imgLogo'),
                ], className='logo col-2'),
                html.Div([
                html.Span('R', style={'color': 'red'}),
                html.Span('ecommandations '),
                html.Span('KNN', style={'color': 'red'}),], className='h1'),
                html.Div([
                dbc.Button('Accueil', outline=True, color="primary", href='/', className='btn btn-outline-primary'),
                dbc.Button("Industrie", outline=True, color="primary", href='/page-1', className='btn btn-outline-primary'),
                dbc.Button('Acteurs & Actrices', outline=True, color="primary", href='/page-2', className='btn btn-outline-primary'),
                dbc.Button('Réalisateurs', outline=True, color="primary", href='/page-3', className='btn btn-outline-primary'),
                dbc.Button('Genres', outline=True, color="primary", href='/page-4', className='btn btn-outline-primary'),
                dbc.Button('Durée', outline=True, color="primary", href='/page-5', className='btn btn-outline-primary'),
                dbc.Button('Recommandations KNN', outline=True, color="primary", href='/page-6', className='btn btn-outline-primary'),
                dbc.Button('Recommandations Cosine', outline=True, color="primary", href='/page-7', className='btn btn-outline-primary'),
                ], className='nav'),
            ]),
                html.Br(),
                dcc.Input(id="input1", type="text", placeholder="Saisir un film pour avoir une recommandation", debounce=True, className='input'),
                html.Div(id="output"),


                html.Div([],id='page-6-content', className='cardContainer'),



             html.Div([
                 html.Span('Les Vac’', className='h3'),
                 html.Span('Cinés!', className='h3', style={'color': 'red'}), 
                 html.P('Vous vous êtes déjà demandé quoi regarder? Heureusement, il existe un service qui peut vous aider à faire le tri entre tous les contenus qui vous sont proposés et qui vous aidera à trouver les films qui correspondent à vos critères. Vous pouvez faire des recherches précises en insérant des mots-clés, des noms de films. Ce service vous est proposé par Gilles, Leila, David, Olivier et Romain', className='col-6 offset-6'),
                 ], className='baner text-white w-100 position-absolute bottom-0 end-0 text-end pe-2'
            ),
        
            
    ], className='text-justify')
])   

@app.callback(Output('page-6-content', 'children'),
              [Input('input1', 'value')])
# def page_6_radios(value):
#     print( f'You have selected {value}')


def search(value):
    # je crée une colonne avec les titres en lower
    df_6000["primaryTitleLower"] = df_6000["primaryTitle"].str.lower()
    
    # je factorise les colonnes qui ne sont pas numriques
   
    list_set = ['actor1', 'origin_country', 'primary_clean']
    for i in list_set:
        df_6000[i + "_num"] = df_6000[i].factorize()[0]
        
     # input   
    film_to_search = value.lower()
    
    # je verifie si le film que j'ai demandé existe
    if df_6000["primaryTitleLower"].isin([film_to_search]).any():
        film = df_6000[df_6000["primaryTitleLower"].isin([film_to_search])]
        film_genre1 = film["genre1"].to_string(index=False)
        film_genre2 = film["genre2"].to_string(index=False)
        df_6000_genre = df_6000[df_6000["genre1"] == film_genre1]
        df_6000_genre = df_6000_genre[df_6000_genre["genre2"] == film_genre2]
        
    # si le film que j'ai demandé n'existe pas, je recommande des films avec le mot clé tapé precedemment et invite à resaisir un film
    else:
        reco = df_6000[df_6000['primaryTitleLower'].str.contains(film_to_search)] 
        
        
        
        searchTitle = reco['primaryTitle'].tolist()
        



        resultSearchTitle = []        

        titles = []

        for e in searchTitle:
            titles.append(e)
            titles.append(html.Br())

        cardMsg = html.Div(
            [
                html.P("Nous n'avons pas trouvé ce film...", className='cardP'), 
                html.P("Nous pouvons vous proposer ces titres de films en fonction de vos critère de recherche, merci de réessayer, avec un de ces films:", className='cardP'), 
                html.H3(titles, className='cardTitleSearch') 
                ], className='cardMsg'
            )
            
        resultSearchTitle.append(cardMsg)
        return resultSearchTitle


    
    # valeurs du film choisi
    film_values=df_6000_genre.loc[df_6000_genre.primaryTitleLower == film_to_search, ['actor1_num', 'origin_country_num', 'primary_clean_num']].values.tolist()
    
    #supprimer le film choisi
    df_6000_without_film =df_6000_genre.drop(df_6000_genre.loc[df_6000_genre['primaryTitleLower']==film_to_search].index)
    
    # je reset l'index
    df_6000_without_film.reset_index(inplace=True)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
    # je garde les variables numerique que je mets dans X
        X = df_6000_without_film[['actor1_num', 'origin_country_num', 'primary_clean_num']]

    # avec 5 voisins les plus proches
        distanceKNN = NearestNeighbors(n_neighbors=5).fit(X)
    
    # le plus proche de movie_user_likes
        neighbours=distanceKNN.kneighbors(film_values)
        pd.set_option('display.max_colwidth', None)
        result = df_6000_without_film.loc[neighbours[1:5][0][0]][["primaryTitle", "startYear", "runtimeMinutes", "averageRating", "actor1",
                                                            "actress1", "director1", "writer1", "genre1", "genre2","genre3", "overview",
                                                            "origin_country", "poster_path", "trailer"]]
        title = result['primaryTitle'].tolist()
        poster = result['poster_path'].tolist()
        genre1 = result['genre1'].tolist()
        averageRating = result['averageRating'].tolist()
        startYear = result['startYear'].tolist()
        trailer = result['trailer'].tolist()
    
    
        recos = []        

        for i in range(0,5):
            
            card = html.Div([html.Div([
                html.A([
            html.Img(
                src=poster[i], className='cardPoster')
    ], href=f'https://www.imdb.com/video/imdb/{trailer[i]}/imdb/embed', target='_blank')]), 
                
                html.H3(title[i], className='cardTitle'), html.P(f"Date de sortie: {startYear[i]}", className='cardStartYear'), html.P(f"Genre: {genre1[i]}", className='cardGenre1'), html.P(f"Note: {averageRating[i]}", className='cardAverageRating')], className='card')
            
            recos.append(card)
        return recos
        


page_7_layout = html.Div([
    dbc.Row([


            html.Div([
                html.Div([
                html.Img(src='assets\img\logo.png', className='img-fluid position-absolute top-0 start-0 imgLogo'),
                ], className='logo col-2'),
                html.Div([
                html.Span('R', style={'color': 'red'}),
                html.Span('ecommandations '),
                html.Span('Cosine', style={'color': 'red'}),], className='h1'),
                html.Div(id='page-7-content'),
                html.Div([
                dbc.Button('Accueil', outline=True, color="primary", href='/', className='btn btn-outline-primary'),
                dbc.Button("Industrie", outline=True, color="primary", href='/page-1', className='btn btn-outline-primary'),
                dbc.Button('Acteurs & Actrices', outline=True, color="primary", href='/page-2', className='btn btn-outline-primary'),
                dbc.Button('Réalisateurs', outline=True, color="primary", href='/page-3', className='btn btn-outline-primary'),
                dbc.Button('Genres', outline=True, color="primary", href='/page-4', className='btn btn-outline-primary'),
                dbc.Button('Durée', outline=True, color="primary", href='/page-5', className='btn btn-outline-primary'),
                dbc.Button('Recommandations KNN', outline=True, color="primary", href='/page-6', className='btn btn-outline-primary'),
                dbc.Button('Recommandations Cosine', outline=True, color="primary", href='/page-7', className='btn btn-outline-primary'),
                ], className='nav'),
            ], className='box'),
                html.Br(),
                dcc.Input(id="input2", type="text", placeholder="Saisir un film pour avoir une recommandation", debounce=True, className='input'),
                html.Div(id="output"),


                html.Div([],id='page-7-content', className='cardContainer'),



             html.Div([
                 html.Span('Les Vac’', className='h3'),
                 html.Span('Cinés!', className='h3', style={'color': 'red'}), 
                 html.P('Vous vous êtes déjà demandé quoi regarder? Heureusement, il existe un service qui peut vous aider à faire le tri entre tous les contenus qui vous sont proposés et qui vous aidera à trouver les films qui correspondent à vos critères. Vous pouvez faire des recherches précises en insérant des mots-clés, des noms de films. Ce service vous est proposé par Gilles, Leila, David, Olivier et Romain', className='col-6 offset-6'),
                 ], className='baner text-white w-100 position-absolute bottom-0 end-0 text-end pe-2'
            ),
        
            
    ], className='text-justify')
])   


@app.callback(Output('page-7-content', 'children'),
              [Input('input2', 'value')])


# fonction user input
def user_input(value):
    # je crée une colonne avec les titres en lower
    df_ml["primaryTitleLower"] = df_ml["primaryTitle"].str.lower()
      
     # input   
    film_to_search = value.lower()
    
    # je verifie si le film que j'ai demandé existe
    if df_ml["primaryTitleLower"].isin([film_to_search]).any():
        film = df_ml[df_ml["primaryTitleLower"].isin([film_to_search])]
        
    # si le film que j'ai demandé n'existe pas, je recommande des films avec le mot clé tapé precedemment et invite à resaisir un film
    else:
        
        reco = df_ml[df_ml['primaryTitleLower'].str.contains(film_to_search)] 
        
        
        searchTitle = reco['primaryTitle'].tolist()
        



        resultSearchTitle = []        

        titles = []

        for e in searchTitle:
            titles.append(e)
            titles.append(html.Br())

        cardMsg = html.Div(
            [
                html.P("Nous n'avons pas trouvé ce film...", className='cardP'), 
                html.P("Nous pouvons vous proposer ces titres de films en fonction de vos critère de recherche, merci de réessayer, avec un de ces films:", className='cardP'), 
                html.H3(titles, className='cardTitleSearch') 
                ], className='cardMsg'
            )
            
        resultSearchTitle.append(cardMsg)
        return resultSearchTitle

    # ajout colonne combinaison des features au df_ml avec la fonction
    df_ml["combined_features"] = df_ml.apply(combine_features,axis=1)

    cv = CountVectorizer()
    count_matrix = cv.fit_transform(df_ml["combined_features"])

    cosine_sim = cosine_similarity(count_matrix)

    # index du film input
    movie_index = df_ml.index[ df_ml['primaryTitle'].str.lower()==film_to_search.lower() ].tolist()[0]

    # liste films similaires
    similar_movies =  list(enumerate(cosine_sim[movie_index]))

    # tri liste ( x[1] = taux proba ) par ordre décroissant de proba
    sorted_similar_movies = sorted(similar_movies,key=lambda x:x[1],reverse=True)[1:] # à partir de 1 pour ne pas prendre le film en input
    
    sorted_similar_movies = [get_title_from_index(element[0]) for element in sorted_similar_movies][0:5]
    
    result = df_ml[df_ml['primaryTitle'].isin(sorted_similar_movies)]
    
    title = result['primaryTitle'].tolist()
    poster = result['poster_path'].tolist()
    genre1 = result['genre1'].tolist()
    averageRating = result['averageRating'].tolist()
    startYear = result['startYear'].tolist()
    trailer = result['trailer'].tolist()   
    
    recos = []        

    for i in range(0,5):
            
            card = html.Div([html.Div([
                html.A([
            html.Img(
                src=poster[i], className='cardPoster')
    ], href=f'https://www.imdb.com/video/imdb/{trailer[i]}/imdb/embed', target='_blank')]), 
                
                html.H3(title[i], className='cardTitle'), html.P(f"Date de sortie: {startYear[i]}", className='cardStartYear'), html.P(f"Genre: {genre1[i]}", className='cardGenre1'), html.P(f"Note: {averageRating[i]}", className='cardAverageRating')], className='card')
            
            recos.append(card)
    return recos




# fonction : combinaison des features
def combine_features(row):
    return str(row['actor1']) +" "+str(row['actor2'])+" "+str(row["actor3"])+" "+str(row["actor4"]) +" "+str(row['actor5']) \
         +" "+str(row['actress1']) +" "+str(row['actress2'])+" "+str(row["actress3"])+" "+str(row["actress4"]) +" "+str(row['actress5']) \
         +" "+str(row['director1']) +" "+str(row['director2'])+" "+str(row["writer1"])+" "+str(row["writer2"]) +" "+str(row['writer3']) \
         +" "+str(row['genre1']) +" "+str(row['genre2'])+" "+str(row["genre3"])+" "+str(row["original_language"])



# fonction récupérer le titre avec l'index
def get_title_from_index(index):
    return df_ml._get_value(index, 'primaryTitle')





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
    elif pathname == '/page-6':
        return page_6_layout
    elif pathname == '/page-7':
        return page_7_layout
    else:
        return index_page
    # You could also return a 404 "URL not found" page here

if __name__ == '__main__':
    app.run_server(debug=False)