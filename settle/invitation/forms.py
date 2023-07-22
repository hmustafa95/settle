from django import forms
from .models import Invitation


class InvitationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'contactus'
        self.fields['email'].widget.attrs['class'] = 'contactus'
        self.fields['location'].widget.attrs['class'] = 'contactus'
        self.fields['date'].widget.attrs['class'] = 'contactus'

    class Meta:
        model = Invitation
        fields = '__all__'
