from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .views import add_photo, edit_photo, details_photo, delete_photo, gallery, confirm_delete_photo

urlpatterns = [
    path('gallery/', gallery, name='gallery'),
    path('add/', add_photo, name='add-photo'),
    path('<int:pk>/', include([
        path('', details_photo, name='details-photo'),
        path('edit/', edit_photo, name='edit-photo'),
        path('delete/', delete_photo, name='delete-photo'),
        path('confirm-delete/', confirm_delete_photo, name='confirm-delete-photo'),
    ])),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
