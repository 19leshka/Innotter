import uuid
from django.db import models
from tag.models import Tag
from user.models import User


class Page(models.Model):
    name = models.CharField(max_length=80)
    uuid = models.CharField(max_length=36, unique=True, default=uuid.uuid4)
    description = models.TextField()
    tags = models.ManyToManyField(Tag, related_name='pages', blank=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pages')
    followers = models.ManyToManyField(User, related_name='follows', blank=True)

    image = models.CharField(max_length=200, null=True, blank=True)

    is_private = models.BooleanField(default=False)
    follow_requests = models.ManyToManyField(User, related_name='requests', blank=True)
    is_blocked = models.BooleanField(default=False)
    unblock_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name
