from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Profile(models.Model):
    def user_directory_path(instance, filename):
        return 'user_{0}/photo/{1}'.format(instance.created_by.id, filename) 

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500)
    photo = models.ImageField(    null=True, blank=True, 
                                  upload_to=user_directory_path)


class Genre(models.Model):
    name = models.CharField(max_length=50, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name',]),
        ]
        

class Tag(models.Model):
    name = models.SlugField(db_index=True)
	
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name',]),
        ]


class Track(models.Model):
    def user_directory_path(instance, filename):
        return 'user_{0}/audio/{1}'.format(instance.created_by.id, filename)
		
    title = models.CharField(max_length=100)
    source = models.FileField(upload_to=user_directory_path)
    desc = models.TextField()
    picture = models.ImageField(    null=True, blank=True, 
                                    upload_to=user_directory_path)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    genre = models.ManyToManyField(Genre)
    tag = models.ManyToManyField(Tag)
	
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
        indexes = [
            models.Index(fields=['title',]),
            models.Index(fields=['created_by',]),
            models.Index(fields=['-created_at',]),
        ]


class Comment(models.Model):
    text = models.TextField(max_length=500)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[0:50]

    class Meta:
        ordering = ['track', '-created_at']
        indexes = [
            models.Index(fields=['track', '-created_at',]),
        ]
        

class Like(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    track = models.ForeignKey(Track, on_delete=models.CASCADE, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.created_by.username + ' liked ' + self.track.title 
	
    class Meta:
        ordering = ['track']
        indexes = [
            models.Index(fields=['track'],),
            models.Index(fields=['created_by', '-created_at',]),
        ]        
        

class Sub(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    to_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    to_id = models.PositiveIntegerField()
    to_object = GenericForeignKey('to_type', 'to_id')
	
    def __str__(self):
        return self.from_user.username + ' subscribed to ' + self.to_object.__str__()
	
    class Meta:
        ordering = ['from_user']
        indexes = [
            models.Index(fields=['from_user', 'to_type',]),
        ]
