
from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile_picture_preview')

    def profile_picture_preview(self, obj):
        if obj.profile_picture:
            return f'<img src="{obj.profile_picture.url}" width="50" height="50" />'
        return ""
    profile_picture_preview.allow_tags = True
    profile_picture_preview.short_description = 'Profile Picture'

admin.site.register(Profile, ProfileAdmin)

