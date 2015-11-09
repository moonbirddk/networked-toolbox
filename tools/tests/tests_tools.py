from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from tools.models import Tool
from tools.utils import generate_upload_path


TEST_PNG_CONTENT = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'


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
        self.assertTemplateUsed(resp, 'tools/add.html')
        self.assertContains(resp, 'Add tool')

    def test_add_tool_post(self):
        empty = {}
        resp = self.client.post(reverse('tools:add'), empty, follow=True)
        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'tools/add.html')
        self.assertContains(resp, 'Add tool')

        test_fh = SimpleUploadedFile('test empty.png', TEST_PNG_CONTENT)
        data = {
            'title': 'our test title',
            'description': 'description test',
            'cover_image': test_fh
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
        self.assertTrue(tool.cover_image)
        self.assertTrue(tool.cover_image.name, 'test empty.png')

    def test_edit_tool_get(self):
        tool = Tool.objects.create(
            title='A title', description='A description')

        resp = self.client.get(reverse('tools:edit', args=(tool.id,)))
        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'tools/edit.html')
        self.assertContains(resp, 'Edit tool')
        self.assertContains(resp, tool.title)
        self.assertContains(resp, tool.description)

    def test_edit_tool_post(self):
        tool = Tool.objects.create(
            title='A title', description='A description')
        test_fh = SimpleUploadedFile('test empty.png', TEST_PNG_CONTENT)
        data = {
            'title': 'our new title',
            'description': 'new description test',
            'cover_image': test_fh,
        }
        resp = self.client.post(
            reverse('tools:edit', args=(tool.id,)), data, follow=True)
        self.assertEqual(
            [('http://testserver/tools/', 302)], resp.redirect_chain)
        self.assertTrue('messages' in resp.context)
        self.assertEqual(
            "You updated a tool", str(list(resp.context['messages'])[0]))
        self.assertContains(resp, data['title'])
        tool = Tool.objects.get(id=tool.id)
        self.assertTrue(tool.cover_image)
        self.assertTrue(tool.cover_image.name, 'test empty.png')

    def test_edit_tool_post_update_file(self):
        test_fh1 = SimpleUploadedFile('test empty1.png', TEST_PNG_CONTENT)
        tool = Tool.objects.create(
            title='A title',
            description='A description',
            cover_image=test_fh1
        )

        empty = {}
        resp = self.client.post(
            reverse('tools:edit', args=(tool.id,)), empty, follow=True)
        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'tools/edit.html')
        self.assertContains(resp, 'Edit tool')

        test_fh2 = SimpleUploadedFile('test empty2.png', TEST_PNG_CONTENT)
        data = {
            'title': 'our new title',
            'description': 'new description test',
            'cover_image': test_fh2,
        }
        resp = self.client.post(
            reverse('tools:edit', args=(tool.id,)), data, follow=True)
        self.assertEqual(
            [('http://testserver/tools/', 302)], resp.redirect_chain)
        self.assertTrue('messages' in resp.context)
        self.assertEqual(
            "You updated a tool", str(list(resp.context['messages'])[0]))
        self.assertContains(resp, data['title'])
        tool = Tool.objects.get(id=tool.id)
        self.assertTrue(tool.cover_image)
        self.assertTrue(tool.cover_image.name, 'test empty2.png')

    def test_edit_tool_post_clear_cover_image(self):
        test_fh = SimpleUploadedFile('test empty.png', TEST_PNG_CONTENT)
        tool = Tool.objects.create(
            title='A title', description='A description', cover_image=test_fh)

        data = {
            'title': 'our new title',
            'description': 'new description test',
            'cover_image-clear': 1,
        }
        resp = self.client.post(
            reverse('tools:edit', args=(tool.id,)), data, follow=True)
        self.assertEqual(
            [('http://testserver/tools/', 302)], resp.redirect_chain)
        self.assertTrue('messages' in resp.context)
        self.assertEqual(
            "You updated a tool", str(list(resp.context['messages'])[0]))
        self.assertContains(resp, data['title'])
        tool = Tool.objects.get(id=tool.id)
        self.assertFalse(tool.cover_image)

    def test_index_get(self):
        resp = self.client.get(reverse('tools:index'))
        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'tools/index.html')
        self.assertContains(resp, 'List of tools')

    def test_show_get(self):
        tool = Tool.objects.create(
            title='A title', description='A description')
        resp = self.client.get(reverse('tools:show', args=(tool.id, )))
        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'tools/show.html')
        self.assertContains(resp, 'Resources')
