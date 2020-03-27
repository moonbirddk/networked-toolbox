import unittest
from django.test import TestCase

from django.contrib.auth.models import User

from tools.models import Tool, ToolFollower, Story

from profiles.models import Profile


class HomePageViewTestCase(TestCase):

    def setUp(self):
        self.test_user = User.objects.create_user('testuser',
            'testuser@localhost', 'testpass')
        self.test_user.first_name='test first'
        self.test_user.last_name='test last'
        """
        test_profile, _ = Profile.objects.get_or_create(user=self.test_user)
        test_profile.bio='test bio'
        test_profile.country='DK'
        self.test_user.save()
        self.another_user = User.objects.create_user('anotheruser',
            'anotheruser@localhost', 'testpass')
        another_profile, _ = Profile.objects.get_or_create(user=self.another_user)
        self.tool_followed = Tool.objects.create(title='test tool',
                description='description', published=True)
        ToolFollower.objects.create(user=self.test_user, tool=self.tool_followed)
        self.tool_not_followed = Tool.objects.create(title='another test tool',
                description='description', published=True)
        self.tool_with_story = Tool.objects.create(title='third test tool',
                description='description', published=True)
        """

    def test_homepage_get(self):
        url = reverse('search:homepage')
        resp = self.client.get(url, follow=True)
        self.assertEqual([], resp.redirect_chain)
        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'search/index.html')


class SearchIndexTestCase(TestCase):

    def setUp(self):
        self.test_user = User.objects.create_user('testuser',
            'testuser@localhost', 'testpass')
        self.test_user.first_name='test first'
        self.test_user.last_name='test last'

    # TODO: Implement a test that shows that a user cannot be found by a search
    # on the users name

    # @unittest.skip("FIXME")
    def test_profile_seachable(self):
        self.test_user.profile = Profile.objects.create()
        self.test_user.profile.save()
        #self.assertTemplateUsed(resp, 'search/index.html')
        print(self.test_user)
