from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    match_id = models.CharField(max_length=30, unique=True)
    title = models.CharField(max_length=100, default="title")
    slug = models.SlugField(unique=True, default="")
    desc = models.TextField(max_length=1000, default="desc")
    venue = models.CharField(max_length=50, default="venue")
    video_file = models.FileField(upload_to="videos/posts", max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (self.match_id)