from posts.models import *
from random import choice, randint
from django.db import connection
from django.core.files import File as DjangoFile

n = 100000

def delete_gt():
	Genre.objects.all().delete()
	Tag.objects.all().delete()
	User.objects.exclude(username='sergey').delete()
	Track.objects.all().delete()

f = open('gen/genre_names_first.txt')
genre_names_first = f.read().split('\n')
f.close()

f = open('gen/genre_names_second.txt')
genre_names_second = f.read().split('\n')
genre_names_second.pop()
f.close()

f = open('gen/nouns.txt')
nouns = f.read().split('\n')
nouns.pop()
f.close()

path_to_pic = "/home/sergey/Изображения/pics/"
path_to_audio = "/home/sergey/Музыка/"

genres = []
tags = []
users = []
profiles = []
comments = []
likes = []
subs = []

def get_random_sentence(n_words):
	sentence = ''.join(choice(nouns) + ' ' for i in range(randint(1,n_words)))
	return sentence

def get_random_subobj():
	return choice([choice(users), choice(genres), choice(tags)])

for gf in genre_names_first:
	for gs in genre_names_second:
		for i in range(int(n/(len(genre_names_first)*len(genre_names_second)))+1):
			genres.append(Genre(name=gf+gs+str(i)))
			tags.append(Tag(name=choice(nouns)+str(randint(1,n))))

Genre.objects.bulk_create(genres)
print('Genres created')
Tag.objects.bulk_create(tags)
print('Tags created')
genres = Genre.objects.all()
tags = Tag.objects.all()

for noun in nouns:
	for i in range(int(n/len(nouns))+1):
		users.append(User(username=noun+str(i), password='12345678'))
User.objects.bulk_create(users)

users = User.objects.filter(profile=None)
print('Users created')

#pics = [
#	DjangoFile(    open('{0}/{1}.jpg'.format(path_to_pic, str(i)), mode='rb'), 
#				   name=str(i)+'.jpg'
#			  ) for i in range(1,25)
#]
#pics.append('')
for new_user in users:
	profiles.append(	Profile(user=new_user, 
						bio=get_random_sentence(20), 
						photo=choice([path_to_pic+str(randint(1,25))+'.jpg','']))
					)
Profile.objects.bulk_create(profiles)
print('Profiles created')

#audiofiles = [
#	DjangoFile(    open('{0}/{1}.jpg'.format(path_to_audio, str(i)), mode='rb'), 
#				   name=str(i)+'.mp3'
#			  ) for i in range(1,8)
#]
for j in range(10):
	tracks = []
	for i in range(n/10):
		track = Track(    title=get_random_sentence(4), 
                      	source=path_to_audio+str(randint(1,5))+'.mp3',
					  	desc=get_random_sentence(20), 
                      	picture=choice([path_to_pic+str(randint(1,25))+'.jpg','']),
					  	created_by=choice(users)
				 	 )
		tracks.append(track)
	Track.objects.bulk_create(tracks)
print('Tracks created')
tracks = Track.objects.all()
#for track in tracks:
#	track.genre.add([choice(genres) for i in range(randint(1,4))])
#	track.tag.add([choice(tags) for i in range(randint(1,5))])

#pics.pop()
#for pic in pics:
#	pic.close()
#for audio in audiofiles:
#	audio.close()

for i in range(n):
	comments.append(Comment(    text=get_random_sentence(20), created_by=choice(users),
				                track_id=choice(tracks)
					       ))
	likes.append(Like(created_by=choice(users), track_id=choice(tracks)))
	subs.append(Sub(from_user=choice(users), to_object=get_random_subobj()))
Comment.objects.bulk_create(comments)
print('Comments created')
Like.objects.bulk_create(likes)
print('Likes created')
Sub.objects.bulk_create(subs)
