from django.test import TestCase

from .utils import generate_upload_path
from .testlib import TEST_PNG_CONTENT


class UtilsTestCase(TestCase):
    def test_generate_upload_path(self):
        actual = generate_upload_path(None, 'some file.jpeg', None)
        self.assertRegex(actual, r'^[a-z0-9]{32}\.jpeg$')

    def test_generate_upload_path_with_dir(self):
        actual = generate_upload_path(None, 'some file.jpeg', 'somedir')
        self.assertRegex(actual, r'^somedir/[a-z0-9]{32}\.jpeg$')