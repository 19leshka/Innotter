from celery import shared_task

from innotter.services import AwsService


@shared_task()
def send_email(data: dict) -> dict:
    return AwsService.send_email(data)
