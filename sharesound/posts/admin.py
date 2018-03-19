from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import *

class ProfileInline(admin.StackedInline):
	model = Profile
	can_delete = False
	verbose_name_plural = 'profiles'

class UserAdmin(BaseUserAdmin):
	inlines = (ProfileInline,)

class TrackAdmin(admin.ModelAdmin):
	raw_id_fields = ('created_by', 'genre', 'tag',)

class CommentAdmin(admin.ModelAdmin):
	raw_id_fields = ('created_by',)

class SubAdmin(admin.ModelAdmin):
	raw_id_fields = ('from_user',)

class GenreAdmin(admin.ModelAdmin):
	pass

class TagAdmin(admin.ModelAdmin):
	pass

class LikeAdmin(admin.ModelAdmin):
	raw_id_fields = ('created_by', 'track',)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Track, TrackAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Sub, SubAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Like, LikeAdmin)
