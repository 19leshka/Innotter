from django.db import models

from page.models import Page
from user.models import User


class Post(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='posts')
    content = models.CharField(max_length=180)
    reply_to = models.ForeignKey('post.Post', on_delete=models.SET_NULL, null=True, blank=True, related_name='replies')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner_post')
    liked_by = models.ManyToManyField(User, related_name='liked_by_post', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content
