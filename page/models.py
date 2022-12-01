from django.db import models
from tag.models import Tag


class Page(models.Model):
    name = models.CharField(max_length=80)
    uuid = models.CharField(max_length=30, unique=True)
    description = models.TextField()
    tags = models.ManyToManyField(Tag, related_name='pages')

    owner = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='pages')
    followers = models.ManyToManyField('user.User', related_name='follows')

    image = models.URLField(null=True, blank=True)

    is_private = models.BooleanField(default=False)
    follow_requests = models.ManyToManyField('user.User', related_name='requests')

    unblock_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

    def create_page(self, name: str, description: str):
        if name is None:
            raise TypeError('Pages must have a name.')

        if description is None:
            raise TypeError('Pages must have a description.')

        page = self.model(name=name, description=description)
        page.save()

        return page
