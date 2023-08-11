from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import get_user_model
from django.contrib.auth import views as auth_views
from .forms import UserCreateForm, UserLoginForm, UserEditForm
from ..common.forms import SubscribeForm

UserModel = get_user_model()


# View for user registration (sign-up)
class UserCreateView(views.CreateView):
    model = UserModel
    form_class = UserCreateForm
    template_name = 'accounts/register-page.html'
    success_url = reverse_lazy('login')  # Redirect to the login page after successful registration


# View for user login
class UserLoginView(auth_views.LoginView):
    form_class = UserLoginForm
    template_name = 'accounts/login-page.html'
    next_page = reverse_lazy('home-page')  # Redirect to the home page after successful login


# View for user logout
class UserLogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('home-page')


# View for displaying user profile details
class UserDetailsView(views.DetailView):
    model = UserModel
    template_name = 'accounts/profile-details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subscribe_form'] = SubscribeForm()
        return context


# View for editing user profile
class UserProfileEditView(views.UpdateView):
    model = UserModel
    form_class = UserEditForm
    template_name = 'accounts/edit-page.html'

    def get_success_url(self):
        return reverse_lazy('profile-details', kwargs={'pk': self.object.pk})


# View for deleting user profile
class UserProfileDeleteView(views.DeleteView):
    model = UserModel
    template_name = 'accounts/delete-page.html'
    success_url = reverse_lazy('home-page')
