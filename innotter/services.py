import logging
import os
import boto3


class AwsService:
    @staticmethod
    def get_credentials():
        credentials = {
            'aws_access_key_id': os.getenv('AWS_ACCESS_KEY_ID'),
            'aws_secret_access_key': os.getenv('AWS_SECRET_KEY'),
        }
        return credentials

    @staticmethod
    def get_client(name: str):
        credentials = AwsService.get_credentials()
        client = boto3.client(name, **credentials)

        if name == 'ses':
            client.verify_email_identity(EmailAddress=os.getenv('EMAIL_HOST_USER'))

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
            response = client_s3.generate_presigned_url('get_object',
                                                        Params={'Bucket': os.getenv('BUCKET_NAME'),
                                                                'Key': key},
                                                        ExpiresIn=3600)
        except:
            return None

        return response
