from django.conf import settings
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core import mail
from django.contrib.auth import get_user_model

from common.testlib import TEST_PNG_CONTENT
from ..models import Tool, Suggestion


class SuggestionTestCase(TestCase):
    def setUp(self):
        self.test_user = get_user_model().objects.create_user('test@localhost',
            'test@localhost')
        self.test_user.set_password('testpass')
        self.test_user.save()
        self.test_tool = Tool.objects.create(
            title='A tool title',
            description='A tool description',
            published=True
        )

    def test_add_suggestion_get(self):
        self.client.login(username='test@localhost', password='testpass')
        url = reverse('tools:add_suggestion', args=('tool', self.test_tool.id))
        resp = self.client.get(url)
        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'tools/add_suggestion.html')
        self.assertContains(resp, 'Add Suggestion')

    def test_add_suggestion_post_to_unpublished(self):
        self.client.login(username='test@localhost', password='testpass')
        self.test_tool.published = False
        self.test_tool.save()
        url = reverse('tools:add_suggestion', args=('tool', self.test_tool.id))
        data = {
            'description': 'test suggestion description',
        }
        resp = self.client.post(url, data, follow=True)
        self.assertEqual(404, resp.status_code)

    def test_add_suggestion_post(self):
        self.client.login(username='test@localhost', password='testpass')
        url = reverse('tools:add_suggestion', args=('tool', self.test_tool.id))
        test_fh = SimpleUploadedFile('test empty.png', TEST_PNG_CONTENT,
                                     content_type='image/png')
        data = {
            'description': 'test suggestion description',
            'attachement': test_fh,
        }
        resp = self.client.post(url, data, follow=True)
        self.assertEqual(
            [('http://testserver/tools/%d/' % self.test_tool.id, 302)],
            resp.redirect_chain)
        self.assertTrue('messages' in resp.context)
        self.assertEqual(
            "Your suggestion has been send to administrator",
            str(list(resp.context['messages'])[0]))
        q = Suggestion.objects\
            .filter(description=data['description'])
        self.assertEqual(1, q.count())
        actual = q[0]
        self.assertEqual(actual.description, data['description'])
        self.assertEqual(actual.related_object, self.test_tool)

        self.assertEqual(len(mail.outbox), 1)
        expected = "New suggestion"
        self.assertEqual([settings.SITE_ADMIN_EMAIL], mail.outbox[0].to)
        self.assertEqual(expected, mail.outbox[0].subject)
        print(mail.outbox[0].body)
        self.assertEqual(actual.related_object.title, self.test_tool.title)
        self.assertIn(self.test_tool.title, mail.outbox[0].body)
        self.assertIn('has sent a suggestion to a tool:', mail.outbox[0].body)
        self.assertIn(self.test_tool.get_absolute_url(), mail.outbox[0].body)
        self.assertIn(actual.author.profile.name(), mail.outbox[0].body)
        self.assertIn(actual.author.email, mail.outbox[0].body)
        self.assertIn(actual.description, mail.outbox[0].body)
        self.assertIn(actual.attachement.url, mail.outbox[0].body)

    def test_delete_tool(self):
        suggestion = Suggestion(
            description='test description',
            related_object=self.test_tool,
            author=self.test_user
        )
        suggestion.save()
        self.test_tool.delete()
        self.assertFalse(Suggestion.objects
                         .filter(description='test description')
                         .exists())

    def test_delete_suggestion(self):
        suggestion = Suggestion(
            description='test description',
            related_object=self.test_tool,
            author=self.test_user
        )
        suggestion.save()
        suggestion.delete()
        self.assertTrue(Tool.objects
                        .filter(id=self.test_tool.id)
                        .exists())
