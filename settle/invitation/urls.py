from django.urls import path
from .views import invite


urlpatterns = [
    path('invite/', invite, name='invite'),
    path('invite/success/', invite, name='invite-success'),
]
