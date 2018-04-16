from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import *

class UserAdmin(admin.ModelAdmin):
	pass

class GenreRelsAdmin(admin.ModelAdmin):
    raw_id_fields = ('genre', 'track',)

class TrackAdmin(admin.ModelAdmin):
	raw_id_fields = ('created_by', 'album')

class CommentAdmin(admin.ModelAdmin):
	raw_id_fields = ('created_by',)

class SubAdmin(admin.ModelAdmin):
	raw_id_fields = ('from_user',)

class GenreAdmin(admin.ModelAdmin):
	pass
    
class TagRelsAdmin(admin.ModelAdmin):
    raw_id_fields = ('tag',)

class TagAdmin(admin.ModelAdmin):
	pass

class LikeAdmin(admin.ModelAdmin):
	raw_id_fields = ('created_by',)
	
class AlbumAdmin(admin.ModelAdmin):
    raw_id_fields = ('created_by',)

admin.site.register(User, UserAdmin)
admin.site.register(Track, TrackAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Sub, SubAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(GenreRelationship, GenreRelsAdmin)
admin.site.register(TagRelationship, TagRelsAdmin)
admin.site.register(Album, AlbumAdmin)
