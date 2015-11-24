from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User

from .models import Profile


TEST_PNG_CONTENT = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'


class ProfilesViewsTestCase(TestCase):

    def setUp(self):
        self.test_user = User.objects.create_user('testuser',
            'testuser@localhost', 'testpass')

    def test_add_profile_get(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('profiles:profile')
        resp = self.client.get(url, follow=True)
        self.assertEqual([], resp.redirect_chain)
        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'profiles/profile.html')
        self.assertContains(resp, 'Your profile')

    def test_add_profile_post(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('profiles:profile')
        empty = {}
        resp = self.client.post(url, empty, follow=True)
        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'profiles/profile.html')
        self.assertContains(resp, 'Your profile')
        test_fh = SimpleUploadedFile(
            'test post empty.png',
            TEST_PNG_CONTENT,
            content_type='image/png'
        )
        data = {
            'first_name': 'test first name',
            'last_name': 'test last name',
            'photo': test_fh
        }

        resp = self.client.post(url, data, follow=True)
        self.assertEqual(200, resp.status_code)
        expected_status = (
            'http://testserver/profiles/your-profile/',
            302
        )
        self.assertEqual([expected_status], resp.redirect_chain)
        self.assertTrue('messages' in resp.context)
        self.assertEqual(
            "You have updated your profile.",
            str(list(resp.context['messages'])[0])
        )

        result = Profile.objects.filter(user=self.test_user)
        self.assertEqual(1, result.count())
        test_profile = result[0]
        self.assertEqual(test_profile.user.first_name, data['first_name'])
        self.assertEqual(test_profile.user.last_name, data['last_name'])
        self.assertTrue(test_profile.photo)
        self.assertTrue(
            test_profile.photo.name,
            'test post empty.png'
        )
