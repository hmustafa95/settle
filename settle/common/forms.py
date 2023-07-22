from django import forms
from .models import Subscribe, Contact


class SubscribeForm(forms.ModelForm):
    email = forms.EmailField(max_length=50, widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class'] = 'subsrib'

    class Meta:
        model = Subscribe
        fields = ['email']


class ContactForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'contactus'
        self.fields['phone'].widget.attrs['class'] = 'contactus'
        self.fields['email'].widget.attrs['class'] = 'contactus'
        self.fields['message'].widget.attrs['class'] = 'textarea'

    class Meta:
        model = Contact
        fields = ['name', 'phone', 'email', 'message']


class SearchForm(forms.Form):
    search_bar = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Search...'
            }
        )
    )
