from django import forms

class MovieForm(forms.Form):
    series_title = forms.CharField(max_length=200)
    released_year = forms.IntegerField()
    certificate = forms.CharField(max_length=10)
    runtime = forms.CharField(max_length=20)
    genre = forms.CharField(max_length=100)
    imdb_rating = forms.FloatField()
    overview = forms.CharField(widget=forms.Textarea)
    meta_score = forms.IntegerField()
    director = forms.CharField(max_length=100)
    star1 = forms.CharField(max_length=100)
    star2 = forms.CharField(max_length=100)
    star3 = forms.CharField(max_length=100)
    star4 = forms.CharField(max_length=100)
    no_of_votes = forms.IntegerField()
    gross = forms.CharField(max_length=20)
    poster_link = forms.URLField()
    
class ReviewForm(forms.Form):
    rating = forms.ChoiceField(choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')])
    comment = forms.CharField(widget=forms.Textarea, required=False)