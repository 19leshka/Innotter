from django.db import models


class Post(models.Model):
    page = models.ForeignKey('page.Page', on_delete=models.CASCADE, related_name='posts')
    content = models.CharField(max_length=180)

    reply_to = models.ForeignKey('post.Post', on_delete=models.SET_NULL, null=True, related_name='replies')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
