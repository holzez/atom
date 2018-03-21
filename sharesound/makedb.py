from posts.models import *
from random import choice, randint
from django.db import connection
from django.core.files import File as DjangoFile
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType

n = 100000
batch_size = 1000

f = open('../gen/genre_names_first.txt')
genre_names_first = f.read().split('\n')
f.close()

f = open('../gen/genre_names_second.txt')
genre_names_second = f.read().split('\n')
genre_names_second.pop()
f.close()

number_unique_genres = len(genre_names_first)*len(genre_names_second)*2

f = open('../gen/nouns.txt')
nouns = f.read().split('\n')
nouns.pop()
f.close()

path_to_pic = "photo"
path_to_audio = "audio"

def get_random_sentence(n_words, fill=[' ']):
	sentence = ''.join(choice(nouns) + choice(fill) for i in range(randint(2, n_words)))
	return sentence

def get_random_obj(content_type):
	if content_type.model == 'tag':
		return choice(tags)['pk']
	elif content_type.model == 'genre':
		return choice(genres)['pk']
	elif content_type.model == 'user':
		return choice(users)['pk']
	elif content_type.model == 'track':
	    return choice(tracks)['pk']
	elif content_type.model == 'comment':
	    return choice(comments)['pk']
		
genres = []
tags = []
users = []
tracks = []
subs = []
comments = []
likes = []
genre_track_rels=[]
tag_track_rels=[]
tag_content_types = ContentType.objects.get(app_label='posts', model='track')
subs_content_types = ContentType.objects.filter(app_label='posts').filter(Q(model='genre') | Q(model='tag') | Q(model='user'))
like_content_types = ContentType.objects.filter(app_label='posts').filter(Q(model='track') | 
                                                                        Q(model='genre') | 
                                                                        Q(model='tag') | 
                                                                        Q(model='comment'
                                                                      ))
'''
for gf in genre_names_first:
    for gs in genre_names_second:
        genres.append(Genre(name="%s %s" % (gf, gs)))
        if gs != '':
            genres.append(Genre(name="%s %s" % (gs, gf)))
        for i in range(int(n/number_unique_genres)):
            genres.append(
                Genre(name="%s %s %s" % (gf, gs, str(i)))
            )
Genre.objects.bulk_create(genres, batch_size)
genres = Genre.objects.all().values('pk')
print('Genres generated')
'''
for noun in nouns:
    for i in range(int(n/len(nouns))+1):
        users.append(
            User(username="%s%s" % (noun, str(i)),
                first_name=choice(nouns),
                last_name=choice(nouns),
                email='%s@%s.%s' % (choice(nouns), choice(nouns), choice(['ru', 'org', 'com'])),
                bio=get_random_sentence(20, fill=[' ', ', ', '. ', '! ', '? ']),
                photo=choice([None, 'photo/{0}.jpg'.format(randint(1,25))])
            )
        )
        tags.append(
            Tag(name="%s%s%s" % (noun, choice([choice(nouns), randint(1,1000), '_']), choice([choice(nouns), randint(0,1000), ''])))
        )
        gf = [choice(genre_names_first), choice(genre_names_second)]
        gs = [choice(genre_names_first), choice(genre_names_second)]
        genres.append(
            Genre(name='{0} {1} {2}'.format(choice(gf), choice([noun, str(i)]), choice(gs)))
        )
Genre.objects.bulk_create(genres, batch_size)
genres = Genre.objects.all().values('pk')
print('Genres generated')
User.objects.bulk_create(users, batch_size)
users = User.objects.all().values('pk')
print('Users generated')
Tag.objects.bulk_create(tags, batch_size)
tags = Tag.objects.all().values('pk')
print('Tags generated') 

for i in range(n):
    tracks.append(
        Track(title=get_random_sentence(5),
            desc=get_random_sentence(20, fill=[' ', ', ', '. ', '! ']),
            source='audio/{0}.mp3'.format(randint(1,5)),
            picture=choice([None,'photo/{0}.jpg'.format(randint(1,25))]),
            created_by_id=choice(users)['pk']
        )
    )
    sub_content_type = choice(subs_content_types)
    sub_object_id = get_random_obj(sub_content_type)
    subs.append(
        Sub(from_user_id=choice(users)['pk'],
            content_type=sub_content_type,
            object_id=sub_object_id
        )
    ) 

Track.objects.bulk_create(tracks, batch_size)
tracks = Track.objects.all().values('pk')
print('Tracks generated')
Sub.objects.bulk_create(subs, batch_size)
print('Subs generated')

for i in range(n):
    comments.append(
        Comment(text=get_random_sentence(30, fill=[' ', ', ', '. ', '! ', '? ']),
            created_by_id=choice(users)['pk'],
            track_id=choice(tracks)['pk']
        )
    )
Comment.objects.bulk_create(comments, batch_size)
comments = Comment.objects.all().values('pk')
print('Comments generated')

for i in range(n):
    like_content_type = choice(like_content_types)
    likes.append(
        Like(created_by_id=choice(users)['pk'],
            content_type=like_content_type,
            object_id=get_random_obj(like_content_type)
        )
    )
    genre_track_rels.append(
        GenreRelationship(genre_id=choice(genres)['pk'], track_id=choice(tracks)['pk'])
    )
    tag_track_rels.append(
        TagRelationship(tag_id=choice(tags)['pk'],
            content_type=tag_content_types,
            object_id=get_random_obj(tag_content_types)
        )
    )
Like.objects.bulk_create(likes, batch_size)
print('Likes generated')
GenreRelationship.objects.bulk_create(genre_track_rels, batch_size)
print('GenreRelationships generated')
TagRelationship.objects.bulk_create(tag_track_rels, batch_size)
print('TagRelationships generated')
