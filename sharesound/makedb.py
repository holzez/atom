from posts.models import *
from random import choice, randint
from django.db import connection
from django.core.files import File as DjangoFile
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType

n = 100000
batch_size = 50000

f = open('../gen/genre_names_first.txt')
genre_names_first = f.read().split('\n')
genre_names_first.pop()
f.close()

f = open('../gen/genre_names_second.txt')
genre_names_second = f.read().split('\n')
f.close()

number_unique_genres = len(genre_names_first)*len(genre_names_second)*2

f = open('../gen/nouns.txt')
nouns = f.read().split('\n')
nouns.pop()
f.close()

path_to_pic = "photo"
path_to_audio = "audio"

def get_capital_letter(word):
    return '{0}{1}'.format(word[0].upper(), word[1:])

def get_random_sentence(n_words, fill=['']):
    noun = choice(nouns)
    sentence = get_capital_letter(noun)
    for i in range(randint(2, n_words)):
        f = choice(fill)
        noun = choice(nouns)
        try:
            ['.', '!', '?'].index(f)
        except ValueError:
            pass
        else:
            noun = get_capital_letter(noun)
        finally:
            sentence = '{0}{1} {2}'.format(sentence, f, noun)
#	sentence = ''.join(choice(nouns) + choice(fill) for i in range(randint(2, n_words)))
    return sentence

def get_random_obj(model):
	if model == 'tag':
		return choice(tags)['pk']
	elif model == 'genre':
		return choice(genres)['pk']
	elif model == 'user':
		return choice(users)['pk']
	elif model == 'track':
	    return choice(tracks)['pk']
	elif model == 'comment':
	    return choice(comments)['pk']
	elif model == 'album':
	    return choice(albums)['pk']
	    
def get_random_pic(blank=True):
    pics = ['photo/{0}.jpg'.format(randint(1,25))]
    if blank:
        pics.append(None)
    return choice(pics)
        
		
genres = []
tags = []
users = []
tracks = []
subs = []
comments = []
likes = []
albums = []
genre_track_rels=[]
tag_track_rels=[]


content_types = ContentType.objects.filter(app_label='posts').values('pk', 'model') 
tag_content_types = [c_type for c_type in content_types if c_type['model'] in ['album', 'track']]
subs_content_types = [c_type for c_type in content_types if c_type['model'] in ['genre', 'tag', 'user']]
comment_content_types = [c_type for c_type in content_types if c_type['model'] in ['album', 'track']]
like_content_types = [c_type for c_type in content_types if c_type['model'] in ['album', 'track', 'genre', 'tag', 'comment']]


for noun in nouns:
    for i in range(int(n/len(nouns))+1):
        users.append(
            User(username="{0}{1}{2}".format(noun, str(i), choice([choice(nouns), ''])),
                password="{0}{1}".format(choice(nouns), randint(1,1000)),
                first_name=get_capital_letter(choice(nouns)),
                last_name=get_capital_letter(choice(nouns)),
                email='%s@%s.%s' % (choice(nouns), choice(nouns), choice(['ru', 'org', 'com'])),
                bio=get_random_sentence(20, fill=['', ',', '.', '!', '?']),
                photo=get_random_pic()
            )
        )
        tags.append(
            Tag(name="%s%s%s" % (noun, choice([choice(nouns), i, '_']), choice([choice(nouns), randint(0,1000)])))
        )
User.objects.bulk_create(users, batch_size)
users = User.objects.all().values('pk')
print('Users generated')
Tag.objects.bulk_create(tags, batch_size)
tags = Tag.objects.all().values('pk')
print('Tags generated') 

for gf in genre_names_first:
    for gs in genre_names_second:
        genres.append(Genre(name="{0} {1}".format(gf, gs)))
        if gs != '':
            genres.append(Genre(name="{0} {1}".format(gs, gf)))
Genre.objects.bulk_create(genres, batch_size)
genres = Genre.objects.all().values('pk')
print('Genres generated')

for i in range(int(n/5)):
    albums.append(
                Album(title=get_random_sentence(5),
                    desc=get_random_sentence(30, fill=['', ',', '.', '!']),
                    cover=get_random_pic(),
                    created_by_id=choice(users)['pk']
                )
            )
Album.objects.bulk_create(albums, batch_size)
albums = Album.objects.all().values('pk', 'created_by_id')
print('Albums generated')

for i in range(int(9*n/10)):
    album = choice(albums)
    tracks.append(
        Track(title=get_random_sentence(5),
            desc=get_random_sentence(20, fill=['', ',', '.', '!']),
            source='audio/{0}.mp3'.format(randint(1,5)),
            picture=get_random_pic(),
            album_id=album['pk'],
            created_by_id=album['created_by_id']
        )
    )

for i in range(int(n/10)):
    tracks.append(
        Track(title=get_random_sentence(5),
            desc=get_random_sentence(20, fill=['', ',', '.', '!']),
            source='audio/{0}.mp3'.format(randint(1,5)),
            picture=get_random_pic(),
            album_id='',
            created_by_id=choice(users)['pk']
        )
    )

Track.objects.bulk_create(tracks, batch_size)
tracks = Track.objects.all().values('pk')
print('Tracks generated')

for i in range(n):
    comment_content_type = choice(comment_content_types)
    comment_object_id = get_random_obj(comment_content_type['model'])
    comments.append(
        Comment(text=get_random_sentence(30, fill=['', ',', '.', '!', '?']),
            created_by_id=choice(users)['pk'],
            content_type_id=comment_content_type['pk'],
            object_id=comment_object_id
        )
    )
    sub_content_type = choice(subs_content_types)
    sub_object_id = get_random_obj(sub_content_type['model'])
    subs.append(
        Sub(from_user_id=choice(users)['pk'],
            content_type_id=sub_content_type['pk'],
            object_id=sub_object_id
        )
    )
Comment.objects.bulk_create(comments, batch_size)
comments = Comment.objects.all().values('pk')
print('Comments generated')
Sub.objects.bulk_create(subs, batch_size)
print('Subs generated')

for i in range(n):
    like_content_type = choice(like_content_types)
    likes.append(
        Like(created_by_id=choice(users)['pk'],
            content_type_id=like_content_type['pk'],
            object_id=get_random_obj(like_content_type['model'])
        )
    )
    genre_track_rels.append(
        GenreRelationship(genre_id=choice(genres)['pk'], track_id=choice(tracks)['pk'])
    )
    tag_content_type=choice(tag_content_types)
    tag_track_rels.append(
        TagRelationship(tag_id=choice(tags)['pk'],
            content_type_id=tag_content_type['pk'],
            object_id=get_random_obj(tag_content_type['model'])
        )
    )
Like.objects.bulk_create(likes, batch_size)
print('Likes generated')
GenreRelationship.objects.bulk_create(genre_track_rels, batch_size)
print('GenreRelationships generated')
TagRelationship.objects.bulk_create(tag_track_rels, batch_size)
print('TagRelationships generated')
