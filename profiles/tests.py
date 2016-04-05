from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from django.contrib.auth import REDIRECT_FIELD_NAME
from http.cookies import Morsel

from .models import Profile


TEST_PNG_CONTENT = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'


class TermsAndConditionsTestCase(TestCase):
    def setUp(self):
        pass

    def test_get_with_next(self):
        url = reverse('tools:list_categories') + '?published=1'
        resp = self.client.get(url, follow=True)
        cookie = self.client.cookies.get('has_accepted_terms')
        self.assertIsInstance(cookie, Morsel)
        self.assertEqual('0', cookie.value)
        self.assertEqual(200, resp.status_code)
        expected_redirect = (
            'http://testserver/profiles/terms-and-conditions'
            '?next=/tools/categories/%3Fpublished%3D1',
            302
        )
        self.assertEqual([expected_redirect], resp.redirect_chain)

    def test_post_with_next_accepted(self):
        url = reverse('profiles:terms_and_conditions') +\
            '?next=/tools/%3Fpublished%3D1%3F'
        data = {
            'accepted': 'on',
            'next': '/tools/categories/?published=1',
            'redirect_field_name': REDIRECT_FIELD_NAME,
        }
        resp = self.client.post(url, data, follow=True)
        cookie = self.client.cookies.get('has_accepted_terms')
        self.assertIsInstance(cookie, Morsel)
        self.assertEqual('1', cookie.value)
        self.assertEqual(200, resp.status_code)
        expected_redirect = (
            'http://testserver/tools/categories/?published=1',
            302
        )
        self.assertEqual([expected_redirect], resp.redirect_chain)

    def test_post_with_next_not_accepted(self):
        url = reverse('profiles:terms_and_conditions') +\
                      '?next=/tools/%3Fpublished%3D1%3F'
        data = {
            'next': '/tools/categories/?published=1',
            'redirect_field_name': REDIRECT_FIELD_NAME,
        }
        resp = self.client.post(url, data, follow=True)
        cookie = self.client.cookies.get('has_accepted_terms')
        self.assertIsInstance(cookie, Morsel)
        self.assertEqual('0', cookie.value)
        self.assertEqual(200, resp.status_code)
        self.assertContains(resp, data['next'])
        self.assertContains(resp, data['redirect_field_name'])
        self.assertTrue('messages' in resp.context)
        self.assertEqual(
            "Please accept Terms and Conditions",
            str(list(resp.context['messages'])[0]))


class ProfilesViewsTestCase(TestCase):

    def setUp(self):
        self.test_user = User.objects.create_user('testuser',
            'testuser@localhost', 'testpass')
        self.test_user.first_name='test first'
        self.test_user.last_name='test last'
        test_profile, _ = Profile.objects.get_or_create(user=self.test_user)
        test_profile.bio='test bio'
        test_profile.country='DK'
        self.test_user.save()
        self.another_user = User.objects.create_user('anotheruser',
            'anotheruser@localhost', 'testpass')
        another_profile, _ = Profile.objects.get_or_create(user=self.another_user)

    def test_show_profile_get(self):
        url = reverse('profiles:show', args=(self.test_user.id,))
        resp = self.client.get(url, follow=True)
        self.assertEqual([], resp.redirect_chain)
        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'profiles/show.html')
        self.assertContains(resp, self.test_user.first_name)
        self.assertContains(resp, self.test_user.last_name)
        self.assertContains(resp, self.test_user.profile.country)
        self.assertContains(resp, self.test_user.profile.country.name)
        self.assertContains(resp, self.test_user.profile.bio)
        self.assertNotContains(resp, 'glyphicon-pencil')
        self.client.login(username='testuser', password='testpass')
        resp = self.client.get(url, follow=True)
        self.assertContains(resp, 'glyphicon-pencil')
        url = reverse('profiles:show', args=(self.another_user.id,))
        resp = self.client.get(url, follow=True)
        self.assertNotContains(resp, 'glyphicon-pencil')

    def test_edit_profile_get(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('profiles:edit')
        resp = self.client.get(url, follow=True)
        self.assertEqual([], resp.redirect_chain)
        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'profiles/edit.html')
        self.assertContains(resp, 'Your profile')
        self.assertContains(resp, self.test_user.first_name)
        self.assertContains(resp, self.test_user.last_name)
        self.assertContains(resp, self.test_user.profile.bio)

    def test_edit_profile_post(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('profiles:edit')
        empty = {}
        resp = self.client.post(url, empty, follow=True)
        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'profiles/show.html')
        test_fh = SimpleUploadedFile(
            'test post empty.png',
            TEST_PNG_CONTENT,
            content_type='image/png'
        )
        data = {
            'first_name': 'test first name',
            'last_name': 'test last name',
            'bio': 'anotther test bio',
            'country': 'NL',
            'photo': test_fh
        }

        resp = self.client.post(url, data, follow=True)
        self.assertEqual(200, resp.status_code)
        expected_status = (
            'http://testserver/profiles/%d/' % self.test_user.id,
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
        self.assertEqual(test_profile.bio, data['bio'])
        self.assertEqual(test_profile.country, data['country'])
        self.assertTrue(test_profile.photo)
        self.assertTrue(
            test_profile.photo.name,
            'test post empty.png'
        )
