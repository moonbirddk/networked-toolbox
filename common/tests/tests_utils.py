from django.test import TestCase
from common.utils import generate_upload_path

from tools.utils import generate_upload_path
from ..models import Tool, ToolCategory, ToolResource


TEST_PNG_CONTENT = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'


class UtilsTestCase(TestCase):
    def test_generate_upload_path(self):
        actual = generate_upload_path(None, 'some file.jpeg', None)
        self.assertRegex(actual, r'^[a-z0-9]{32}\.jpeg$')

    def test_generate_upload_path_with_dir(self):
        actual = generate_upload_path(None, 'some file.jpeg', 'somedir')
        self.assertRegex(actual, r'^somedir/[a-z0-9]{32}\.jpeg$')