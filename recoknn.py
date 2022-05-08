def search(value):
    # je crée une colonne avec les titres en lower
    df_6000["primaryTitleLower"] = df_6000["primaryTitle"].str.lower()
    
    # je factorise les colonnes qui ne sont pas numriques
   
    list_set = ['actor1', 'actress1', 'genre1','origin_country']
    for i in list_set:
        df_6000[i + "_num"] = df_6000[i].factorize()[0]
        
     # input   
    film_to_search = value.lower()
    
    # je verifie si le film que j'ai demandé existe
    if df_6000["primaryTitleLower"].isin([film_to_search]).any():
        film = df_6000[df_6000["primaryTitleLower"].isin([film_to_search])]
        
    # si le film que j'ai demandé n'existe pas, je recommande des films avec le mot clé tapé precedemment et invite à resaisir un film
    else:
        reco = df_6000[df_6000['primaryTitleLower'].str.contains(film_to_search)] 
        
        
        
        searchTitle = reco['primaryTitle'].tolist()
        



        resultSearchTitle = []        

        searchTitle
            
        cardMsg = html.Div([html.P("Nous n'avons pas trouvé ce film...", className='cardP'), html.P("Nous pouvons vous proposer ces titres de films en fonction de vos critère de recherche, merci de réessayer, avec un de ces films:", className='cardP'), html.H3(f"{'-----'.join(searchTitle)}", className='cardTitleSearch')], className='cardMsg')
            
        resultSearchTitle.append(cardMsg)
        return resultSearchTitle


    
    # valeurs du film choisi
    film_values=df_6000.loc[df_6000.primaryTitleLower == film_to_search, ['actor1_num', 'actress1_num', 'genre1_num','origin_country_num']].values.tolist()
    
    #supprimer le film choisi
    df_6000_without_film =df_6000.drop(df_6000.loc[df_6000['primaryTitleLower']==film_to_search].index)
    
    # je reset l'index
    df_6000_without_film.reset_index(inplace=True)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
    # je garde les variables numerique que je mets dans X
        X = df_6000_without_film[['actor1_num', 'actress1_num', 'genre1_num','origin_country_num']]

    # avec 5 voisins les plus proches
        distanceKNN = NearestNeighbors(n_neighbors=5).fit(X)
    
    # le plus proche de movie_user_likes
        neighbours=distanceKNN.kneighbors(film_values)
        pd.set_option('display.max_colwidth', None)
        result = df_6000_without_film.loc[neighbours[1:5][0][0]][["primaryTitle", "startYear", "runtimeMinutes", "averageRating", "actor1",
                                                            "actress1", "director1", "writer1", "genre1", "genre2","genre3", "overview",
                                                            "origin_country", "poster_path"]]
        title = result['primaryTitle'].tolist()
        poster = result['poster_path'].tolist()
        genre1 = result['genre1'].tolist()
        averageRating = result['averageRating'].tolist()
        startYear = result['startYear'].tolist()
        
    
        recos = []        

        for i in range(0,5):
            
            card = html.Div([html.Div([html.Img(src=poster[i], className='cardPoster')]), html.H3(title[i], className='cardTitle'), html.P(f"Date de sortie: {startYear[i]}", className='cardStartYear'), html.P(f"Genre: {genre1[i]}", className='cardGenre1'), html.P(f"Note: {averageRating[i]}", className='cardAverageRating')], className='card')
            
            recos.append(card)
        return recos