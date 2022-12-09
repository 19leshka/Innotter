import logging
import os
import boto3
from botocore.exceptions import ClientError


class AwsService:
    @staticmethod
    def upload_file(file_path: str, key: str) -> str:
        credentials = {
            'aws_access_key_id': os.getenv('AWS_ACCESS_KEY_ID'),
            'aws_secret_access_key': os.getenv('AWS_SECRET_KEY'),
        }
        client_s3 = boto3.client('s3', **credentials)
        client_s3.upload_fileobj(file_path, Bucket=os.getenv('BUCKET_NAME'), Key=key)

        return key

    @staticmethod
    def get_file_url(key: str = None):
        credentials = {
            'aws_access_key_id': os.getenv('AWS_ACCESS_KEY_ID'),
            'aws_secret_access_key': os.getenv('AWS_SECRET_KEY'),
        }
        client_s3 = boto3.client('s3', **credentials)

        try:
            response = client_s3.generate_presigned_url('get_object',
                                                        Params={'Bucket': os.getenv('BUCKET_NAME'),
                                                                'Key': key},
                                                        ExpiresIn=3600)
        except:
            return None

        return response
