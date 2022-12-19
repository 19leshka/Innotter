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

        print(table)

        return table

    @staticmethod
    def get_item(item_id: int) -> dict:
        table = DynamoDBService.get_table()
        response = table.get_item(
            Key={
                'id': item_id
            }
        )

        return response

    @staticmethod
    def put_item(data: dict) -> dict:
        table = DynamoDBService.get_table()
        response = table.put_item(
            Item={
                'id': data['id'],
                'total_likes': 0,
                'total_followers': 0,
                'total_posts': 0
            }
        )
        return response

    @staticmethod
    def delete_item(data: dict) -> dict:
        table = DynamoDBService.get_table()
        response = table.delete_item(
            Item={
                'id': data['id']
            }
        )

        return response

    @staticmethod
    def update_stat(data):
        table = DynamoDBService.get_table()
        response = table.update_item(
            Key={
                'id': int(data.get('id'))
            },
            UpdateExpression=f"SET #{data.get('value')} = #{data.get('value')} + :decrement",
            ExpressionAttributeNames={
                f"#{data.get('value')}": f"{data.get('value')}"
            },
            ExpressionAttributeValues={
                ":decrement": data.get('count')
            }
        )
        return response