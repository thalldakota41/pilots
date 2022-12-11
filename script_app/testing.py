 df = pd.DataFrame(recom_show_data, columns = ['Title', 'Genre', 'Show_id'])
    
    
    
    # creates a column to hold the combined strings
    df['important_features'] = df['Title'].astype(str) + df['Genre'].astype(str)
    
    
    # convert the text to a matrix of token counts
    cm = CountVectorizer().fit_transform(df['important_features'])
    
    # get the cosine similarity matrix from the count matrix
    cs =  cosine_similarity(cm)

    # df.set_index('Show_id', inplace=True)
    
    # Get the title from show_obj = Show.objects.get(id=id)
    matched_title_id = df[df.Title == show_obj]['Show_id'].values[0]
    
# Creates a list of enumerations for the similarity score [ (matched_title_id, similarity score), (...) ]
scores = list(enumerate(cs[matched_title_id]))
   
    # sorts the list
    sorted_scores = sorted(scores, key= lambda x:x[1], reverse = True)
    # sorts scores at position 1 and up excluding position 0 which is the original title show
    sorted_scores = sorted_scores[1:]
    
    # Create a loop to print first 15 similar movies
    j = 0
    print('The 15 most recommended movies to', show_obj, 'are:\n')
    for item in sorted_scores:
        show_title = df[df.Show_id == item[0]]['Title'].values
        j = j+1
        if j>14:
            break
        
    #     # fetching API data with recommendation results
        for i in show_title:
            recom_api_data = requests.get(F"https://api.themoviedb.org/3/tv/{i}?api_key={api_key}&language=en-US")
            print(show_title)
