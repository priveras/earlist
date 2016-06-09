from django import forms
 
class PostForm(forms.Form):
    title = forms.CharField(max_length=200)
    slogan = forms.CharField(max_length=200)
    body = forms.CharField(widget=forms.Textarea)
    link = forms.URLField(max_length=200)
    # image_url = forms.URLField(max_length=200)
    image_file = forms.FileField(label='Selecciona un archivo')
    city = forms.CharField(max_length=200)

class EventForm(forms.Form):
    title = forms.CharField(max_length=200)
    body = forms.CharField(max_length=200)
    link = forms.URLField(max_length=200)
    image_file = forms.FileField(label='Selecciona un archivo')
    cover_file = forms.FileField(label='Selecciona un archivo')
    date_time = forms.DateTimeField()

class JobForm(forms.Form):
    title = forms.CharField(max_length=200)
    company = forms.CharField(max_length=200)
    link = forms.URLField(max_length=200)
    image_url = forms.URLField(max_length=200)