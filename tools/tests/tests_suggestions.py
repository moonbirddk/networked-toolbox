from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core import mail

from tools.utils import generate_upload_path
from ..models import Tool, ToolCategory, ToolResource, Suggestion
from django.contrib.auth import get_user_model


TEST_PNG_CONTENT = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'


class SuggestionTestCase(TestCase):
    def setUp(self):
        self.test_user = get_user_model().objects.create_user('test@localhost',
            'test@localhost')
        self.test_user.set_password('testpass')
        self.test_user.save()
        self.test_tool = Tool.objects.create(
            title='A tool title',
            description='A tool description'
        )

    def test_add_suggestion_get(self):
        self.client.login(username='test@localhost', password='testpass')
        url = reverse('tools:add_suggestion', args=('tool', self.test_tool.id))
        resp = self.client.get(url)
        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'tools/add_suggestion.html')
        self.assertContains(resp, 'Add suggestion')

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
        self.assertEqual(expected, mail.outbox[0].subject)
        print(mail.outbox[0].body)
        self.assertIn(self.test_tool.get_absolute_url(), mail.outbox[0].body)
        self.assertIn(actual.attachement.url, mail.outbox[0].body)
        self.assertIn(actual.author.email, mail.outbox[0].body)
        self.assertIn(actual.description, mail.outbox[0].body)
