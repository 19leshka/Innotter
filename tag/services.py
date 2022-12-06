from django.http import HttpRequest
from tag.models import Tag


class TagService:
    @staticmethod
    def process_tags(request: HttpRequest) -> list:
        tags_id = []
        if tags := request.data.pop('tags', None):
            existing_tags = Tag.objects.filter(name__in=tags)
            for tag in existing_tags:
                tags_id.append(tag.id)
                tags.remove(tag.name)
            bulk_list = list()
            [bulk_list.append(Tag(name=tag)) for tag in tags]
            bulk_msj = Tag.objects.bulk_create(bulk_list)
            [tags_id.append(new_tag.id) for new_tag in bulk_msj]
        return tags_id
