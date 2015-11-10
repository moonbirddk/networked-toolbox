from django.test import TestCase
from django.db.models import FileField

from tools.templatetags.toolstags import css_filefield


class CssFileFieldTestCase(TestCase):

    def test_css_filefield_mp4(self):
        ff = FileField(name="somename.mp4")
        self.assertEqual('fa-file-video-o', css_filefield(ff))

    def test_css_filefield_jpg(self):
        ff = FileField(name="somename.jpg")
        self.assertEqual('fa-file-image-o', css_filefield(ff))

    def test_css_filefield_mp3(self):
        ff = FileField(name="somename.mp3")
        self.assertEqual('fa-audio-o', css_filefield(ff))

    def test_css_filefield_text(self):
        ff = FileField(name="somename.txt")
        self.assertEqual('fa-file-text-o', css_filefield(ff))

    def test_css_filefield_docx(self):
        ff = FileField(name="somename.docx")
        self.assertEqual('fa-file-text-o', css_filefield(ff))

    def test_css_filefield_unknown(self):
        ff = FileField(name="somename.xyz")
        self.assertEqual('fa-file-text-o', css_filefield(ff))
