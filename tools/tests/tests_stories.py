
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User, Group
from django_countries import countries
import bleach

from ..models import Tool, Story


def create_tool(title, content):
    return


class StoriesViewsTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        return super(StoriesViewsTestCase, cls).setUpClass()

    def setUp(self):
        self.test_user = User.objects.create(username='testuser')
        self.test_user.set_password('testpass')
        self.test_user.save()
        self.tool = Tool.objects.create(title='title',
                description='description', published=True)

    def test_add_story_get(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('tools:add_story', args=(self.tool.id, ))
        resp = self.client.get(url)
        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'tools/add_story.html')
        self.assertContains(resp, 'Add story')

    def test_add_empty_story_post(self):
        self.client.login(username='testuser', password='testpass')
        empty = {}
        url = reverse('tools:add_story', args=(self.tool.id, ))
        resp = self.client.post(url, empty, follow=True)
        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'tools/add_story.html')
        self.assertContains(resp, 'Add story')

    def test_add_story_post(self):
        self.client.login(username='testuser', password='testpass')
        data = {
            'title': 'our test title',
            'content': '𐍈' * 5000,
            'tool_id' : self.tool.id
        }
        url = reverse('tools:add_story', args=(self.tool.id, ))
        resp = self.client.post(url, data, follow=True)
        self.assertEqual(
            [('http://testserver/tools/%d/' % self.tool.id, 302)],
            resp.redirect_chain)
        self.assertTrue('messages' in resp.context)
        self.assertEqual(
            "You created a story", str(list(resp.context['messages'])[0]))

        self.assertEqual(Story.objects.count(), 1)
        story = Story.objects.all()[0]
        self.assertEqual(story.title, data['title'])
        self.assertEqual(story.content, data['content'])

    def test_tool_show_get(self):
        story_content = '<a href="#">content</a>'
        story = Story.objects.create(title='test story', content=story_content,
                country='DK', tool_id=self.tool.id, user_id=self.test_user.id)
        resp = self.client.get(reverse('tools:show', args=(self.tool.id, )))
        self.assertEqual(200, resp.status_code)
        self.assertContains(resp, 'Stories')
        self.assertContains(resp, story.title)
        self.assertNotContains(resp, story.content)
        self.assertContains(resp, bleach.clean(story.content, tags=[],
            strip=True, strip_comments=True))
        self.assertContains(resp, self.test_user.profile.short_name())
        self.assertContains(resp, story.country.name)

    def test_show_story_get(self):
        story = Story.objects.create(title='test story', content='test content',
                country='DK', tool_id=self.tool.id, user_id=self.test_user.id)
        related_story = Story.objects.create(title='related story', content='related content',
                country='DK', tool_id=self.tool.id, user_id=self.test_user.id)
        resp = self.client.get(reverse('tools:show_story', args=(story.id, )))
        self.assertEqual(200, resp.status_code)
        self.assertContains(resp, story.title)
        self.assertContains(resp, story.content)
        self.assertContains(resp, story.country.name)
        self.assertContains(resp, 'Contributor')
        self.assertContains(resp, self.test_user.profile.name())
        self.assertContains(resp, self.tool.title)
        self.assertContains(resp, 'Related stories')
        self.assertContains(resp, related_story.title)
        self.assertContains(resp, related_story.content)
