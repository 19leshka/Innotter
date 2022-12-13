import os
import boto3

from page.models import Page
from user.models import User


class AwsService:
    @staticmethod
    def get_credentials():
        credentials = {
            'aws_access_key_id': os.getenv('AWS_ACCESS_KEY_ID'),
            'aws_secret_access_key': os.getenv('AWS_SECRET_KEY'),
            'region_name': os.getenv('AWS_DEFAULT_REGION'),
        }
        return credentials

    @staticmethod
    def get_client(name: str):
        credentials = AwsService.get_credentials()
        client = boto3.client(name, **credentials)

        return client

    @staticmethod
    def upload_file(file_path: str, key: str) -> str:
        client_s3 = AwsService.get_client('s3')
        client_s3.upload_fileobj(file_path, Bucket=os.getenv('BUCKET_NAME'), Key=key)

        return key

    @staticmethod
    def get_file_url(key: str = None):
        client_s3 = AwsService.get_client('s3')

        try:
            response = client_s3.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': os.getenv('BUCKET_NAME'),
                    'Key': key
                },
                ExpiresIn=os.getenv('EXPIRES_IN')
            )
        except:
            return None

        return response

    @staticmethod
    def send_email(data: dict) -> dict:
        client_ses = AwsService.get_client('ses')

        emails = list(Page.objects.values_list('followers__email', flat=True).filter(pk=data['page']))
        user = User.objects.get(pk=data['owner'])
        page = Page.objects.get(pk=data['page'])
        message = f"New post by {str(user.username)} on {str(page.name)}."

        response = client_ses.send_email(
            Source=os.getenv('HOST_EMAIL'),
            Destination={
                "ToAddresses": emails,
            },
            Message={
                "Body": {
                    "Text": {
                        "Data": message,
                    }
                },
                "Subject": {
                    "Data": "New post.",
                },
            },
        )

        return response
