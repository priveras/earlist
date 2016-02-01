from django import forms
 
class PostForm(forms.Form):
    title = forms.CharField(max_length=256)
    link = forms.CharField(max_length=256)
    slug = forms.CharField(max_length=256)
    created_at = forms.DateTimeField()