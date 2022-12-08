import os

import boto3


class AwsService:
    @staticmethod
    def upload_file(file_path: str, key: str) -> str:
        credentials = {
            'region_name': os.getenv('AWS_DEFAULT_REGION'),
            'endpoint_url': f"http://{os.getenv('HOSTNAME_EXTERNAL')}:",
            'aws_access_key_id': os.getenv('AWS_ACCESS_KEY_ID'),
            'aws_secret_access_key': os.getenv('AWS_SECRET_KEY'),
        }

        try:
            client = boto3.client('s3', **credentials)
            bucket = client.create_bucket(
                Bucket=os.getenv('BUCKET_NAME'),
                CreateBucketConfiguration={
                    'LocationConstraint': os.getenv('AWS_DEFAULT_REGION')
                }
            )

        except client.exceptions.BucketAlreadyOwnedByYou:
            resource = boto3.resource('s3', **credentials)
            bucket = resource.Bucket(name=os.getenv('BUCKET_NAME'))

        with open(file_path, 'rb') as data:
            bucket.put_object(Key=key, Body=data)

        return key
