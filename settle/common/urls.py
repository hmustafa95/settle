from django.urls import path
from .views import home_page, contact, about, couple, search, subscribe_view


urlpatterns = [
    path('', home_page, name='home-page'),
    path('contact/', contact, name='contact'),
    path('about/', about, name='about'),
    path('couple/', couple, name='couple'),
    path('search/', search, name='search'),
    path('subscribe/', subscribe_view, name='subscribe'),
]
