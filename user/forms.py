from django import forms
from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('match_id','title','slug','desc','venue','video_file','user')