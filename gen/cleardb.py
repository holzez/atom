from posts.models import *

def cleardb():
	User.objects.exclude(username='sergey').delete()
	Genre.objects.all().delete()
	Tag.objects.all().delete()
	Comment.objects.all().delete()
	Album.objects.all().delete()
	Sub.objects.all().delete()
cleardb()
