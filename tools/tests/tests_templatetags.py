from django.test import TestCase
from django.db.models import FileField

from tools.templatetags.toolstags import css_filefield
from tools.templatetags.partition_slice import partition, partition_horizontal


class CssFileFieldTestCase(TestCase):

    def test_css_filefield_mp4(self):
        ff = FileField(name="somename.mp4")
        self.assertEqual('fa-file-video-o', css_filefield(ff))

    def test_css_filefield_jpg(self):
        ff = FileField(name="somename.jpg")
        self.assertEqual('fa-file-image-o', css_filefield(ff))

    def test_css_filefield_mp3(self):
        ff = FileField(name="somename.mp3")
        self.assertEqual('fa-file-audio-o', css_filefield(ff))

    def test_css_filefield_text(self):
        ff = FileField(name="somename.txt")
        self.assertEqual('fa-file-text-o', css_filefield(ff))

    def test_css_filefield_docx(self):
        ff = FileField(name="somename.docx")
        self.assertEqual('fa-file-text-o', css_filefield(ff))

    def test_css_filefield_unknown(self):
        ff = FileField(name="somename.xyz")
        self.assertEqual('fa-file-text-o', css_filefield(ff))


class PartitionSliceTestCase(TestCase):

    def test_partition(self):
        l = range(10)

        expected = [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]
        actual = partition(l, 5)
        self.assertEqual(expected, actual)

        expected = [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9]]
        actual = partition(l, 4)
        self.assertEqual(expected, actual)

        expected = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
        actual = partition(l, 3)
        self.assertEqual(expected, actual)

        expected = [[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]]
        actual = partition(l, 2)
        self.assertEqual(expected, actual)

        expected = [[0], [1], [2], [3], [4], [5], [6], [7], [8], [9]]
        actual = partition(l, 1)
        self.assertEqual(expected, actual)

    def test_partition_horizontal(self):
        l = range(2)
        expected = [[0], [1], []]
        actual = partition_horizontal(l, 3)
        self.assertEqual(expected, actual)

        l = range(3)
        expected = [[0], [1], [2]]
        actual = partition_horizontal(l, 3)
        self.assertEqual(expected, actual)

        l = range(4)
        expected = [[0, 3], [1], [2]]
        actual = partition_horizontal(l, 3)
        self.assertEqual(expected, actual)

        l = range(1, 11)
        expected = [[1, 4, 7, 10], [2, 5, 8], [3, 6, 9]]
        actual = partition_horizontal(l, 3)
        self.assertEqual(expected, actual)
