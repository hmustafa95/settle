from django import forms


from .models import Photo


class PhotoCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'contactus'
        self.fields['photo'].widget.attrs['class'] = 'contactus'
        self.fields['location'].widget.attrs['class'] = 'contactus'
        self.fields['description'].widget.attrs['class'] = 'textarea'

    class Meta:
        model = Photo
        exclude = ['user']

    def save(self, commit=True, user=None):
        instance = super().save(commit=False)
        if user:
            instance.user = user
        if commit:
            instance.save()
        return instance


class PhotoEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'contactus'
        self.fields['location'].widget.attrs['class'] = 'contactus'
        self.fields['description'].widget.attrs['class'] = 'textarea'

    class Meta:
        model = Photo
        exclude = ['photo', 'user']

    def save(self, commit=True, user=None):
        instance = super().save(commit=False)
        if user:
            instance.user = user
        if commit:
            instance.save()
        return instance
