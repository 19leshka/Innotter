import os
import boto3


class DynamoDBService:
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
        credentials = DynamoDBService.get_credentials()
        client = boto3.client(name, **credentials)

        return client

    @staticmethod
    def get_resource(name: str):
        credentials = DynamoDBService.get_credentials()
        resource = boto3.resource(name, **credentials)

        return resource

    @staticmethod
    def get_table():
        client_dynamo = DynamoDBService.get_client('dynamodb')
        resource_dynamo = DynamoDBService.get_resource('dynamodb')

        try:
            table = client_dynamo.create_table(
                AttributeDefinitions=[
                    {
                        'AttributeName': 'id',
                        'AttributeType': 'N'
                    },
                ],
                TableName=os.getenv('DYNAMODB_TABLE_NAME'),
                KeySchema=[
                    {
                        'AttributeName': 'id',
                        'KeyType': 'HASH'
                    },
                ],

                BillingMode='PAY_PER_REQUEST',
            )
        except client_dynamo.exceptions.ResourceInUseException:
            table = resource_dynamo.Table(os.getenv('DYNAMODB_TABLE_NAME'))

        return table

    @staticmethod
    def get_item():
        table = DynamoDBService.get_table()
        response = table.get_item(
            Key={'AttributeName': {'S': 'Page'}}
        )

        return response

    @staticmethod
    def put_item(page: str):
        table = DynamoDBService.get_table()
        print(page)
        response = table.put_item(
            Item={
                'id': page['id'],
                'total_likes': 0,
                'total_folowers': 0,
                'total_posts': 0
            }
        )
        print(response)
        return response

    @staticmethod
    def delete_item(page: str):
        table = DynamoDBService.get_table()
        response = table.delete_item(
            Item={
                'id': page['id']
            }
        )

        return response

    @staticmethod
    def add_post(page: str):
        table = DynamoDBService.get_table()
        response = table.update_item(
            Key={
                'id': page['page']
            },
            UpdateExpression="SET #total_posts = #total_posts + :increment",
            ExpressionAttributeNames={
                "#total_posts": "total_posts"
            },
            ExpressionAttributeValues={
                ":increment": 1
            }
        )
        return response

    @staticmethod
    def delete_post(page: str):
        table = DynamoDBService.get_table()
        response = table.update_item(
            Key={
                'id': page['id']
            },
            UpdateExpression="SET #total_posts = #total_posts - :decrement",
            ExpressionAttributeNames={
                "#total_posts": "total_posts"
            },
            ExpressionAttributeValues={
                ":decrement": 1
            }
        )
        return response

    @staticmethod
    def add_like(page: str):
        table = DynamoDBService.get_table()
        response = table.update_item(
            Key={
                'id': page['id']
            },
            UpdateExpression="SET #total_likes = #total_likes + :increment",
            ExpressionAttributeNames={
                "#total_likes": "total_likes"
            },
            ExpressionAttributeValues={
                ":increment": 1
            }
        )
        return response

    @staticmethod
    def delete_like(page: str):
        table = DynamoDBService.get_table()
        response = table.update_item(
            Key={
                'id': page['id']
            },
            UpdateExpression="SET #total_likes = #total_likes - :decrement",
            ExpressionAttributeNames={
                "#total_likes": "total_likes"
            },
            ExpressionAttributeValues={
                ":decrement": 1
            }
        )
        return response
