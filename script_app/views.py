from email.mime import base
import pprint
from pkgutil import get_data
from pydoc import pager
from unittest import result
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
from .models import *
# (
#     Creator,
#     Tag,
#     Show,
#     Comment
# )
import json
from django.core.paginator import Paginator
from django.db.models import Q
import requests
from pprint import pp, pprint


api_key = ""

def main(request):
    pk = Show.objects.all()
    return render(request, 'main.html', {'pk':pk})



def index(request):
    # grabs all objects in database from Show model class
    post =  Show.objects.all().order_by('title')
    
   
    #loops and matches all database objects with TVDB json data

    
    
    for lists in post:            
        data = requests.get(F"https://api.themoviedb.org/3/search/tv?api_key={api_key}&language=en-US&page=1&include_adult=false&query={lists}")
        
        r = data.json()
        
        # grabs title value from api  
        api_title = r['results'][0]['name']
        # grabe poster path value from api
        api_poster = r['results'][0]['poster_path']
        # grabs id value from api 
        api_id = r['results'][0]['id']

        show_data = {}
        #appends all search results to empty show_data dict.
        show_data[api_title] = {'poster_path':api_poster, 'id':api_id}
        pprint(show_data)

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

    # Pagination
    page_number = request.GET.get('page', 1)
    paginator = Paginator(post, 15) # Show 15 pilots per page.
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
        'post': post,
        
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
    
    show_info = api_show_url.json()
    #pprint(show_info)
    
    context = {'show':show_obj, 'show_info':show_info}
    return render(request, 'show_page.html', context)



# nav bar extras 
    
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