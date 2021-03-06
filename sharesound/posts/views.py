from django.core.serializers import serialize
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, HttpResponse, JsonResponse
from posts.models import *
from django.db.models import Q, Count
from sharesound import settings
from itertools import chain
from operator import attrgetter
from django.contrib.auth.decorators import login_required
import math
import json

ITEMS_PER_PAGE = 21

def get_page(request):
    page = request.GET.get('page') or 1
    
    try:
        return int(page)
    except:
        raise Http404
        
def filter_track_list(request, tracks):
    title = request.GET.get('title')
    author = request.GET.get('author')
    album = request.GET.get('album')
    search_url = ''
    search_dict = {}
    
    if title is not None and title != '':
        tracks = tracks.filter(title__icontains=title)
        search_url = '{0}&title={1}'.format(search_url, title)
        search_dict['title'] = title
    if author is not None and author != '':
        tracks = tracks.filter(created_by__username__icontains=author)
        search_url = '{0}&author={1}'.format(search_url, author)
        search_dict['author'] = author
    if album is not None and album != '':
        tracks = tracks.filter(album__title__icontains=album)
        search_url = '{0}&album={1}'.format(search_url, album)
        search_dict['album'] = album
        
    return {   'tracks': tracks,
               'search_url': search_url,
               'search_dict': search_dict,
           }
        

def posts_list(request):
    
    return render(
        request, 'posts/posts_list.html',
        {
            'nav_posts_is': 'active',
            'title': 'Список песен',
        }        
    )
    
def post_detail(request, post_id):
    try:
        track = Track.objects.prefetch_related('created_by', 'tags', 'genre', 'likes', 'album', 'comments').get(pk=post_id)
    except Track.DoesNotExist:
        raise Http404
    #track = get_object_or_404(Track, pk=post_id)
    
    comments = track.comments.select_related().prefetch_related('likes', 'created_by')
    
    return render(
        request, 'posts/post_detail.html',
        {
            'post': track,
            'comments': comments,
            'nav_posts_is': 'active',
        }
    )
    
def subs_track_list(request):
    if request.user.is_authenticated:
        page = get_page(request)

        number_of_pages = 100
        return render(
            request, 'posts/sub_posts_list.html',
            {
                'nav_sub_posts_is': 'active',
            }
        )
    else:
        return redirect('posts_list', permanent=False)
        
def genre_list(request):
    page = get_page(request)
    genres = Genre.objects.all()[ITEMS_PER_PAGE*(page-1):ITEMS_PER_PAGE*page].prefetch_related('likes', 'subs', 'track_set')
    genre_count = 1640
    number_of_pages = math.ceil(genre_count/ITEMS_PER_PAGE)
    return render(
        request, 'posts/genre_list.html',
        {
            'genre_list': genres,
            'page': page,
            'number_of_pages': number_of_pages,
            'nav_genres_is': 'active',
        }
    )
    
def genre_post_list(request, genre_id):
    page = get_page(request)
    genre = get_object_or_404(Genre, pk=genre_id)
    tracks = Track.objects.filter(genrerelationship__genre_id=genre_id)
    
    filtered_list = filter_track_list(request, tracks)
    
    tracks = filtered_list['tracks']
    
    track_list = tracks[ITEMS_PER_PAGE*(page-1):ITEMS_PER_PAGE*page].prefetch_related('created_by', 'album', 'likes', 'comments')
    
    tracks_count = 1000
    number_of_pages = math.ceil(tracks_count/ITEMS_PER_PAGE)
    return render(
        request, 'posts/posts_list.html',
        {
            'posts_list': track_list,
            'page': page,
            'number_of_pages': number_of_pages,
            'search_url': filtered_list['search_url'],
            'search_dict': filtered_list['search_dict'],
            'nav_genres_is': 'active',
            'title': "Жанр '{0}' - Список песен".format(genre.name)
        }
    )
    
def tag_list(request):
    page = get_page(request)
    tags = Tag.objects.all()[ITEMS_PER_PAGE*(page-1):ITEMS_PER_PAGE*page]
    tag_count = 100100
    number_of_pages = math.ceil(tag_count/ITEMS_PER_PAGE)
    return render(
        request, 'posts/tag_list.html',
        {
            'tag_list': tags,
            'page': page,
            'number_of_pages': number_of_pages,
            'nav_tags_is': 'active',
        }
    )
    
def tag_post_list(request, tag_id):
    return HttpResponse("Tag")
    
def user_list(request):
    page = get_page(request)

    username_search = request.GET.get('username')
    name_search = request.GET.get('name')    
    search_url = ''
    search_dict = {}
    users = User.objects.all()
    
    if username_search is not None and username_search != '':
        users = users.filter(username__icontains=username_search)
        search_url = '{0}&username={1}'.format(search_url, username_search)
        search_dict['username'] = username_search
    if name_search is not None and name_search != '':
        name_sep = name_search.split(' ')
        for name_part in name_sep:
            users = users.filter(Q(first_name__icontains=name_part) | Q(last_name__icontains=name_part))
        search_url = '{0}&name={1}'.format(search_url, name_search)
        search_dict['name'] = name_search
    
    user_count = 100000
    number_of_pages = math.ceil(user_count/ITEMS_PER_PAGE)
    user_list = users[(page-1)*ITEMS_PER_PAGE:page*ITEMS_PER_PAGE].prefetch_related('subs', 'track_set')
    
    #user_list = []
    user_content = ContentType.objects.get_for_model(User)
    #for user in users:
    #    subs_count = Sub.objects.filter(content_type=user_content, object_id=user.id).count()
    #    user_list.append({'user': user, 'subs_count': subs_count}) 
    
    return render(
        request, 'posts/user_list.html',
        {
            'user_list': user_list,
            'page': page,
            'number_of_pages': number_of_pages,
            'search_url': search_url,
            'search_dict': search_dict,
            'nav_users_is': 'active',
        }
    )
    
def user_detail(request, username):
    user = get_object_or_404(User, username=username)
    
    return render(
        request, 'posts/user_detail.html',
        {
            'user': user,
            'nav_users_is': 'active',
        }
    )
    
def album_list(request):
    return render(
        request, 'posts/album_list.html'
    )

def sub_post_list_json(request):
    page = get_page(request)
    subs_id = request.user.sub_set.prefetch_related('content_object__track_set', 'content_object__tag__track_set').values('id')
        
    tracks = Track.objects.all()
    
    tag_tracks = tracks.filter(tags__tag__subs__in=subs_id).select_related('created_by', 'album').prefetch_related('likes', 'comments')
    genre_tracks = tracks.filter(genre__subs__in=subs_id).select_related('created_by', 'album').prefetch_related('likes', 'comments')
    user_tracks = tracks.filter(created_by__subs__in=subs_id).select_related('created_by', 'album').prefetch_related('likes', 'comments')
    
    tracks = sorted(chain(user_tracks, genre_tracks, tag_tracks), key=attrgetter('created_at'), reverse=True)[(page-1)*ITEMS_PER_PAGE:page*ITEMS_PER_PAGE]
    
    likes = []
    result = []
    for track in tracks:
        picture = ''
        if track.picture:
            picture = track.picture.url
        result.append({ 'id': track.id, 
                        'title': track.title, 
                        'created_at': track.created_at, 
                        'picture': picture,
                        'created_by__username': track.created_by.username
                    })
        likes.append( { 'id': track.id, 'likes_count': track.likes.count(), 'comments_count': track.comments.count() } ) 
    
    return JsonResponse({'tracks': result, 'rates': likes}, safe=False)
    
def post_list_json(request):
    page = get_page(request)

    tracks = Track.objects.all()
    
    filtered_list = filter_track_list(request, tracks)
    tracks = filtered_list['tracks']
        
    tracks = tracks[ITEMS_PER_PAGE*(page-1):ITEMS_PER_PAGE*page].select_related('created_by', 'album').prefetch_related('likes', 'comments')
    result = list(tracks.values('id','title','created_at','album','created_by__username', 'picture', 'desc'))
    likes = []
    for track in tracks:
        likes.append({ 'id': track.id, 'likes_count': track.likes.count(), 'comments_count': track.comments.count() })
        
    return JsonResponse({'posts': result, 'rates': likes}, safe=False)

def album_list_json(request):
    page = get_page(request)
    
    title_search = request.GET.get('title')
    author_search = request.GET.get('author')
    albums = Album.objects.all()
    
    if title_search is not None and title_search != '':
        albums = albums.filter(title__icontains=title_search)
        
    if author_search is not None and author_search != '':
        albums = albums.filter(created_by__username__icontains=author_search)
    
    albums = albums[ITEMS_PER_PAGE*(page-1):ITEMS_PER_PAGE*page].select_related('created_by').prefetch_related('likes', 'track_set', 'comments')

    result = list(albums.values('id', 'title', 'created_at', 'created_by__username'))
    rates = []
    for album in albums:
        rates.append({'id': album.id, 'likes_count': album.likes.count(), 'comments_count': album.comments.count(), 'track_count': album.track_set.count()})
        
    return JsonResponse({'albums': result, 'rates': rates}, safe=False)
