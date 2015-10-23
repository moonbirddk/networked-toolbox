from django.test import TestCase
from django.core.urlresolvers import reverse
from .models import Tool

# Create your tests here.

class HomeViewTestCase(TestCase):
    def test_home_get(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(200, resp.status_code)

class ToolsViewsTestCase(TestCase):
    def setUp(self):
        pass

    def test_add_tool_get(self):
        resp = self.client.get(reverse('tools:add_tool'))
        self.assertEqual(200, resp.status_code)

    def test_add_tool_post(self):
        data = {
            'title': 'our test title',
            'description': 'description test',
        }
        resp = self.client.post(reverse('tools:add_tool'), data, follow=True)
        self.assertEqual([('http://testserver/', 302)], resp.redirect_chain)
        self.assertTrue('messages' in resp.context)
        self.assertEqual("You created a tool", str(list(resp.context['messages'])[0]))

        self.assertEqual(Tool.objects.count(), 1)
        tool = Tool.objects.all()[0]
        self.assertEqual(tool.title,data['title'])
        self.assertEqual(tool.description,data['description'])

