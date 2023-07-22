from django.urls import path, include

from .views import UserCreateView, UserLoginView, UserLogoutView, UserProfileEditView, UserDetailsView, \
    UserProfileDeleteView

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/<int:pk>/', include([
        path('', UserDetailsView.as_view(), name='profile-details'),
        path('edit/', UserProfileEditView.as_view(), name='profile-edit'),
        path('delete/', UserProfileDeleteView.as_view(), name='profile-delete'),
    ])),
]
