from django.contrib import admin
from .models import Photo


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'date_of_publication', 'user')
    list_filter = ('date_of_publication', 'user')
    search_fields = ('title', 'location', 'user__username')
    ordering = ('-date_of_publication',)
    readonly_fields = ('date_of_publication',)


admin.site.register(Photo, PhotoAdmin)
