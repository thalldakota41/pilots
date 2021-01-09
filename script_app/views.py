from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
from .models import *
import json
from django.core.paginator import Paginator
from django.db.models import Q


def main(request):
    pk = Pilot.objects.all()

    return render(request, 'main.html', {'pk':pk})

def index(request):
    
    post =  Pilot.objects.all().order_by('id')

    # Search Filter
    search = request.GET.get('search')

    if search != '' and search is not None:
        post = post.filter(Q(title__icontains=search) | Q(writer__icontains=search)).distinct()
    
    # Ajax/js search
    if 'term' in request.GET:
        term = request.GET.get('term')
        qs = Pilot.objects.filter(Q(title__icontains=term) | Q(writer__icontains=term)).distinct()[:10] #limits ten objects displayed with ajax
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
        'search': search
        }
 

    return render(request, 'index.html', context)

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

