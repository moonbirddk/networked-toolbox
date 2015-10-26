from django.test import TestCase
from django.core.urlresolvers import reverse
from .models import Tool
from .utils import generate_upload_path


class UtilsTestCase(TestCase):
    def test_generate_upload_path(self):
        actual = generate_upload_path(None, 'some file.jpeg', None)
        self.assertRegex(actual, r'^[a-z0-9]{32}\.jpeg$')

    def test_generate_upload_path_with_dir(self):
        actual = generate_upload_path(None, 'some file.jpeg', 'somedir')
        self.assertRegex(actual, r'^somedir/[a-z0-9]{32}\.jpeg$')


class HomeViewTestCase(TestCase):

    def test_home_get(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(200, resp.status_code)


class ToolsViewsTestCase(TestCase):

    def setUp(self):
        pass

    def test_add_tool_get(self):
        resp = self.client.get(reverse('tools:add'))
        self.assertEqual(200, resp.status_code)
        self.assertContains(resp, 'Add tool')

    def test_add_tool_post(self):
        empty = {}
        resp = self.client.post(reverse('tools:add'), empty, follow=True)
        self.assertEqual(200, resp.status_code)
        self.assertContains(resp, 'Add tool')

        data = {
            'title': 'our test title',
            'description': 'description test',
        }
        resp = self.client.post(reverse('tools:add'), data, follow=True)
        self.assertEqual(
            [('http://testserver/tools/', 302)], resp.redirect_chain)
        self.assertTrue('messages' in resp.context)
        self.assertEqual(
            "You created a tool", str(list(resp.context['messages'])[0]))

        self.assertEqual(Tool.objects.count(), 1)
        tool = Tool.objects.all()[0]
        self.assertEqual(tool.title, data['title'])
        self.assertEqual(tool.description, data['description'])

    def test_edit_tool_get(self):
        tool = Tool.objects.create(
            title='A title', description='A description')

        resp = self.client.get(reverse('tools:edit', args=(tool.id,)))
        self.assertEqual(200, resp.status_code)
        self.assertContains(resp, 'Edit tool')
        self.assertContains(resp, tool.title)
        self.assertContains(resp, tool.description)

    def test_edit_tool_post(self):
        tool = Tool.objects.create(
            title='A title', description='A description')

        empty = {}
        resp = self.client.post(
            reverse('tools:edit', args=(tool.id,)), empty, follow=True)
        self.assertEqual(200, resp.status_code)
        self.assertContains(resp, 'Edit tool')

        data = {
            'title': 'our new title',
            'description': 'new description test',
        }
        resp = self.client.post(
            reverse('tools:edit', args=(tool.id,)), data, follow=True)
        self.assertEqual(
            [('http://testserver/tools/', 302)], resp.redirect_chain)
        self.assertTrue('messages' in resp.context)
        self.assertEqual(
            "You updated a tool", str(list(resp.context['messages'])[0]))
        self.assertContains(resp, data['title'])

    def test_index_get(self):
        resp = self.client.get(reverse('tools:index'))
        self.assertEqual(200, resp.status_code)
        self.assertContains(resp, 'List of tools')

