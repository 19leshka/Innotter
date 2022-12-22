import unittest
from unittest.mock import patch

from microservice.services import DynamoDBService


class TestDynamoDBServiceMock(unittest.TestCase):

    @patch('microservice.services.DynamoDBService.put_item')
    def test_put_item(self, mock_put_item):
        mock_put_item.return_value = {
                'id': 0,
                'total_likes': 0,
                'total_followers': 0,
                'total_posts': 0
            }

        result = DynamoDBService.put_item({'id': 0})

        self.assertEqual(result, {
                'id': 0,
                'total_likes': 0,
                'total_followers': 0,
                'total_posts': 0
            })

    @patch('microservice.services.DynamoDBService.update_stat')
    def test_update_stat_cases(self, mock_update_stat):
        test_cases = (
            {
                'expected': {
                    'id': 0,
                    'total_likes': 0,
                    'total_followers': 0,
                    'total_posts': 1
                },
                'arguments': {
                    'id': 0,
                    'value': 'total_posts',
                    'count': 1
                }
            },
            {
                'expected': {
                    'id': 0,
                    'total_likes': 0,
                    'total_followers': 2,
                    'total_posts': 1
                },
                'arguments': {
                    'id': 0,
                    'value': 'total_followers',
                    'count': 2
                }
            },
            {
                'expected': {
                    'id': 0,
                    'total_likes': 1,
                    'total_followers': 2,
                    'total_posts': 1
                },
                'arguments': {
                    'id': 0,
                    'value': 'total_likes',
                    'count': 1
                }
            },
            {
                'expected': {
                    'id': 0,
                    'total_likes': 1,
                    'total_followers': 1,
                    'total_posts': 1
                },
                'arguments': {
                    'id': 0,
                    'value': 'total_followers',
                    'count': -1
                }
            },
        )

        for test_case in test_cases:
            mock_update_stat.return_value = test_case['expected']
            result = DynamoDBService.update_stat(**test_case['arguments'])
            self.assertEqual(result, test_case['expected'])

    @patch('microservice.services.DynamoDBService.get_item')
    def test_get_item(self, mock_get_item):
        mock_get_item.return_value = {
            'id': 0,
            'total_likes': 2,
            'total_followers': 3,
            'total_posts': 5
        }

        result = DynamoDBService.get_item(0)

        self.assertEqual(result, {
            'id': 0,
            'total_likes': 2,
            'total_followers': 3,
            'total_posts': 5
        })

    @patch('microservice.services.DynamoDBService.delete_item')
    def test_delete_item(self, mock_delete_item):
        mock_delete_item.return_value = None
        result = DynamoDBService.delete_item({'id': 0})
        self.assertEqual(result, None)

