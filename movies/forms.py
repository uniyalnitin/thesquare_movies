from django import forms
from django.forms import ModelForm
from django.shortcuts import reverse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Row, Column, Submit, HTML

from .models import Movie, Actor, Director, Genre

class MovieForm(ModelForm):
    class Meta:
        model = Movie
        fields = ('imdb_id', 'title', 'year', 'plot', 'language', 'poster', 'poster_url','rating', 'country', 'genre', 'actors', 'directors')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('imdb_id', css_class='form-group col-md-3 mb-0'),
                Column('title', css_class='form-group col-md-3 mb-0'),
                Column('year', css_class='form-group col-md-3 mb-0'),
                Column('language', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('country', css_class='form-group col-md-3 mb-0'),
                Column('rating', css_class='form-group col-md-3 mb-0'),
                Column('poster_url', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('poster', css_class='form-group col-md-3 mb-0'),
                Column('genre', css_class='form-group col-md-3 mb-0'),
                Column('actors', css_class='form-group col-md-3 mb-0'),
                Column('directors', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            HTML('<img src="{{ poster.url }}" />'),
            'plot',
            Submit('submit', 'Save')
        )

class GenreForm(ModelForm):
    class Meta:
        model = Genre
        fields = ('name',)

class DirectorForm(ModelForm):
    class Meta:
        model = Director
        fields = ('name',)

class ApiForm(forms.Form):
    imdb_id = forms.CharField(max_length=64, required=False)
    title = forms.CharField(max_length=100,required=False)
    year = forms.IntegerField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('imdb_id', css_class='form-group col-md-3 mb-0'),
                Column('title', css_class='form-group col-md-3 mb-0'),
                Column('year', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Save')
        )

    def clean(self):
        cleaned_data = super(ApiForm, self).clean()
        imdb_id = cleaned_data.get('imdb_id')
        title = cleaned_data.get('title')
        if not imdb_id and not title:
            raise forms.ValidationError('You have to write something!')