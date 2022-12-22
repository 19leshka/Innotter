import unittest
from unittest.mock import patch

from innotter.services import AwsService


class TestAwsServiceMock(unittest.TestCase):

    @patch('innotter.services.AwsService.upload_file')
    def test_upload_file(self, mock_upload_file):
        mock_upload_file.return_value = 'user1'

        result = AwsService.upload_file('filepath')

        self.assertEqual(result, 'user1')

    @patch('innotter.services.AwsService.get_file_url')
    def test_get_file(self, mock_get_file_url):
        mock_get_file_url.return_value = 'link'

        result = AwsService.get_file_url('user1')

        self.assertEqual(result, 'link')

    @patch('innotter.services.AwsService.send_email')
    def send_email(self, mock_send_email):
        mock_send_email.return_value = 'done'

        result = AwsService.put_item('email')

        self.assertEqual(result, 'done')

