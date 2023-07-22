from django.contrib.auth import forms as auth_forms, get_user_model
from django import forms

UserModel = get_user_model()


class UserCreateForm(auth_forms.UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Enter your password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm your password'

    class Meta:
        model = UserModel
        fields = ('username', 'email')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter your username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
        }


class UserLoginForm(auth_forms.AuthenticationForm):
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'current-password',
                'placeholder': 'Password',
            }
        )
    )


class UserEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['profile_picture'].widget.attrs['class'] = 'form-control'
        self.fields['spouse_first_name'].widget.attrs['class'] = 'form-control'
        self.fields['spouse_last_name'].widget.attrs['class'] = 'form-control'
        self.fields['date_of_marriage'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = UserModel
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'email',
            'profile_picture',
            'spouse_first_name',
            'spouse_last_name',
            'date_of_marriage',
        )

        exclude = ('password',)

        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter your username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter your first name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter your last name'}),
            'profile_picture': forms.URLInput(attrs={'placeholder': 'Enter your profile picture'}),
            'spouse_first_name': forms.TextInput(attrs={'placeholder': 'Enter your spouse first name'}),
            'spouse_last_name': forms.TextInput(attrs={'placeholder': 'Enter your spouse last name'}),
            'date_of_marriage': forms.DateInput(attrs={'placeholder': 'Enter your date of marriage'}),
        }
