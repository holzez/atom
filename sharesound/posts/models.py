from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from .validators import validate_audiofile_extension, get_valid_audio_extensions
from django.db.models import F
import os

def get_directory(instance, filename):
    ext = os.path.splitext(filename)[1]
    audio_extensions = get_valid_audio_extensions()
    if ext.lower() in audio_extensions:
        directory = 'audio'
    else:
        directory = 'photo'
    try:
        username = instance.created_by.username
    except AttributeError:
        username = instance.username
    return '{0}/{1}/{2}'.format(username, directory, filename)


class User(AbstractUser):
    bio = models.TextField(max_length=500)
    photo = models.ImageField(
        upload_to=get_directory,  #!!!!
        null=True, blank=True
    )
    
    subs = GenericRelation('Sub')

    class Meta(AbstractUser.Meta):
        ordering = ['username']
        indexes = [
            models.Index(fields=['username',]),
            models.Index(fields=['email',]),
            models.Index(fields=['first_name', 'last_name', ]),
        ]


class Album(models.Model):
    title = models.CharField(max_length=100)
    desc = models.TextField()
    cover = models.ImageField(upload_to=get_directory, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    tags = GenericRelation('TagRelationship')
    likes = GenericRelation('Like')
    comments = GenericRelation('Comment')
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['title',]),
            models.Index(fields=['-created_at',]),
            models.Index(fields=['created_by',]),
        ]
    

class Genre(models.Model):
    name = models.CharField(max_length=50)
    
    likes = GenericRelation('Like')
    subs = GenericRelation('Sub')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name',]),
        ]

        
class GenreRelationship(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    track = models.ForeignKey('Track', on_delete=models.CASCADE)
    
    def __str__(self):
        return '"{0}" is {1}'.format(self.track.title, self.genre.name)
    
    class Meta:
        ordering = ['genre']
        indexes = [
            models.Index(fields=['genre',]),
            models.Index(fields=['track',]),
        ]


class Tag(models.Model):
    name = models.SlugField(db_index=True)
    
    likes = GenericRelation('Like')
    subs = GenericRelation('Sub')
	
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name',]),
        ]

        
class TagRelationship(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    def __str__(self):
        return '"{0}" was tagged: {1}'.format(self.content_object.__str__(), self.tag.name)
    
    class Meta:
        ordering = ['tag']
        indexes = [
            models.Index(fields=['tag',]),
            models.Index(fields=['content_type', 'object_id',]),
        ]


class Track(models.Model):		
    title = models.CharField(max_length=100)
    desc = models.TextField(help_text='Write a description of the track.')
    genre = models.ManyToManyField(Genre, through=GenreRelationship)
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    source = models.FileField(upload_to=get_directory, validators=[validate_audiofile_extension])
    picture = models.ImageField(null=True, blank=True, upload_to=get_directory)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    tags = GenericRelation('TagRelationship')
    likes = GenericRelation('Like')
    comments = GenericRelation('Comment')
	
    def __str__(self):
        return '{0} - "{1}"'.format(self.created_by.username, self.title)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['title',]),
            models.Index(fields=['created_by',]),
            models.Index(fields=['-created_at',]),
        ]


class Comment(models.Model):
    text = models.TextField(max_length=500)
    
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    likes = GenericRelation('Like')

    def __str__(self):
        return self.text[0:50]

    class Meta:
        ordering = ['content_type', 'object_id', '-created_at']
        indexes = [
            models.Index(fields=['content_type', 'object_id' , '-created_at',]),
        ]
        

class Like(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return '{0} liked {1}: "{2}"'.format(self.created_by.username, self.content_type.model, self.content_object.__str__()) 
	
    class Meta:
        ordering = ['content_type', 'object_id']
        indexes = [
            models.Index(fields=['content_type', 'object_id'],),
            models.Index(fields=['created_by', '-created_at',]),
        ]        
        

class Sub(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
	
    def __str__(self):
        return '{0} subscribed to {1}: {2}'.format(self.from_user.username, self.content_type, self.content_object.__str__())
	
    class Meta:
        ordering = ['from_user']
        indexes = [
            models.Index(fields=['from_user',]),
            models.Index(fields=['content_type', 'object_id',]),
        ]
