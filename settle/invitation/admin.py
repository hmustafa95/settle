from django.contrib import admin
from .models import Invitation


class InvitationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'location', 'date')
    list_filter = ('date',)
    search_fields = ('name', 'email', 'location')
    ordering = ('-date',)
    readonly_fields = ('date',)


admin.site.register(Invitation, InvitationAdmin)
