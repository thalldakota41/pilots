from email.mime import base
import pprint
from pkgutil import get_data
from pydoc import pager
from turtle import title
from unittest import result
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
from .models import *
import json
from django.core.paginator import Paginator
from django.db.models import Q
import requests
from pprint import pp, pprint
import urllib.parse
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from rest_framework import routers, serializers, viewsets
from rest_framework.pagination import LimitOffsetPagination



api_key = ""
base_url = 'https://api.themoviedb.org/3/search/tv'

def main(request):
    pk = Show.objects.all()
    return render(request, 'main.html', {'pk':pk})



def index(request):
    # grabs all objects in database from Show model class
    post =  Show.objects.all().order_by('title')
    
    
   
    #loops and matches all database objects with TVDB json data

    api_data = {}
    
    for lists in post:            
        data = requests.get(F'{base_url}?api_key={api_key}&language=en-US&page=1&include_adult=false&query={lists}')

        r = data.json()
        
        # grabs title value from api  
        api_title = r['results'][0]['name']
        # grabe poster path value from api
        api_poster = r['results'][0]['poster_path']
        # grabs id value from api 
        api_id = r['results'][0]['id']

        
        #appends all search results to empty api_data dict.
        api_data[api_title] = {'poster_path':api_poster, 'id':api_id} #add stuff in the for loop
    
    
    # Search Filter
    search = request.GET.get('search')

    if search != '' and search is not None:
        post = post.filter(Q(title__icontains=search) | Q(creators__icontains=search) | Q(tag__icontains=search)).distinct()
    
    # Ajax/js search
    if 'term' in request.GET:
        term = request.GET.get('term')
        qs = Show.objects.filter(Q(title__icontains=term) | Q(creators__icontains=term) | Q(tag__icontains=term)).distinct()[:10] #limits ten objects displayed with ajax
        results = list()
        for title in qs:
            results.append(title.title)  
        return JsonResponse(results, safe=False)

    # merges api_data and post var into a new data stucture called show_data
    # show_data is a list of two element tuples, the first being
    # ... the api_data dict for the show (poster_path and id)
    # the second is the model from the "post" collection. 
    show_data = []
    for show in post:
        show_data.append( (api_data[show.title], show) )

    # Pagination
    page_number = request.GET.get('page', 1)
    paginator = Paginator(show_data, 15) # Show 15 pilots per page.
    page = paginator.get_page(page_number)

    if page.has_next():
        next_url = f'?page={page.next_page_number()}'
    else:
        next_url = ''

    if page.has_previous():
        prev_url = f'?page={page.previous_page_number()}'
    else: 
        prev_url = ''

    context= {
        'page': page,
        'next_page_url': next_url, 
        'prev_page_url': prev_url,
        'search': search,
        'show_data': show_data, #passes show data along 
        
                }
    return render(request, 'index.html', context)

def creator_page(request, id):
    
    creator_obj = Creator.objects.get(id=id)
    
    # api call to the search url to obtain the "creator's" id for an integer input for the following api url
    api_url = requests.get(f'https://api.themoviedb.org/3/search/person?api_key={api_key}&language=en-US&page=1&include_adult=false&query={creator_obj}')
    
    creator_name = api_url.json()
    # grabs the id of 'creator' from the tmdb api
    creator_tmdb_id = creator_name['results'][0]['id']
    #grabs json object for the specific creator page. 
    api_person_url = requests.get(F"https://api.themoviedb.org/3/person/{creator_tmdb_id}?api_key={api_key}&language=en-US")

    creator_info = api_person_url.json()
    #pprint(creator_info)    


    context = { 
        "creator":creator_obj,
        'creator_info':creator_info,
    }
    return render(request, "creator_page.html", context)



def show_page(request, id):
    show_obj = Show.objects.get(id=id)
    
    # api call to the search url to obtain the "show's" id for an integer input for the following api url
    show_url = requests.get(F"https://api.themoviedb.org/3/search/tv?api_key={api_key}&language=en-US&page=1&include_adult=false&query={show_obj}")

    show_info = show_url.json()
    
    # grabs the id of 'show' from the tmdb api
    show_tmdb_id = show_info['results'][0]['id']
    
    #grabs json object for the specific 'show' page. 
    api_show_url = requests.get(F"https://api.themoviedb.org/3/tv/{show_tmdb_id}?api_key={api_key}&language=en-US")
    
    #returns a json object of the result data
    show_info = api_show_url.json()

    # fetches all the show objects that are displayed as self.title
    recom_show_data = []
    fetch = Show.objects.all()
   
    # loops through each show object
    for show_title in fetch:
       
        #grabs all genre tags that belong to each show object with a manytomany class model named Tag
        genre_data = show_title.tag.all()
        
        # grabs all element ids
        show_title_id = show_title.id
        
        recom_show_data.append((show_title, genre_data, show_title_id))
    
    
    df = pd.DataFrame(recom_show_data, columns = ['Title', 'Genre', 'Show_id'])
    
    #check for any missing values
    check = df.isnull().values.any()
    
    # create a column to hold the combined strings
    df['important_features'] = df['Title'].astype(str) + df['Genre'].astype(str)
    
    # convert the text into a matrix of token counts
    cm = CountVectorizer().fit_transform(df['important_features'])
    
    # get the cosine similarity matrix the count token 
    cs = cosine_similarity(cm)
    
    # finds the movie's index in pd DataFrame
    matched_show_id = df[df.Title == show_obj]['Show_id'].index[0]

    # create a list of enumerations for the similarity scores
    scores = list(enumerate(cs[matched_show_id]))
    
    # sort the list
    sorted_scores = sorted(scores, key= lambda x:x[1], reverse = True)
   
    # sorts scores at position 1 and up excluding position 0 which is the original title show
    sorted_scores = sorted_scores[1:]
    
    # creates a loop to print the first 15 similar movies
    show_title_list = []
    recom_api_data_dict = {}
    j=0
    for item in sorted_scores:
        show_title = df[df.index == item[0]]['Title'].values[0]
        #print(j+1, show_title)
        j = j+1
        if j > 15: 
            break
        
        show_title_list.append(show_title)

    # fetching API data with recommendation results
    for i in show_title_list:
        recom_api_data = requests.get(F"https://api.themoviedb.org/3/search/tv?api_key={api_key}&language=en-US&page=1&include_adult=false&query={i}").json()
        # grabs title value from api  
        api_title = recom_api_data['results'][0]['name']
        # grabe poster path value from api
        api_poster = recom_api_data['results'][0]['poster_path']
        # grabs id value from api 
        api_id = recom_api_data['results'][0]['id']

        #appends all search results to empty api_data dict.
        recom_api_data_dict[api_title] = {'poster_path':api_poster, 'id':api_id} #add stuff in the for loop
    pprint(recom_api_data_dict)
        

    context = {'show':show_obj, 'show_info':show_info}
    return render(request, 'show_page.html', context)
    
def about(request):
    return render(request, 'about.html')

def comment(request):
    return render(request, 'comment.html')

def comment_submit(request):
    if request.method == "POST":

        name=request.POST['name']
        email=request.POST['email']
        message=request.POST['message']
            
        comment = Comment.objects.create(name=name, email=email, message=message)
        if comment.is_valid():
            comment.save()
            return redirect('/')
    return redirect('/')