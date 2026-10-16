from django import forms
from .models import Movie

class MovieForm(forms.ModelForm):
    class Meta :
        model = Movie
        fields = ["title","release_year","description", "poster"]

        widgets = {"description": forms.Textarea(attrs={"rows":4}),}