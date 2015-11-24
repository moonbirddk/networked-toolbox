from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User, Group

from ..models import Tool, ToolCategory, ToolResource


TEST_PNG_CONTENT = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'


class HomeViewTestCase(TestCase):

    def test_home_get(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(200, resp.status_code)


class ToolsViewsTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        return super(ToolsViewsTestCase, cls).setUpClass()

    def setUp(self):
        self.test_admin = User.objects.create(username='testadmin')
        self.test_admin.set_password('testpass')
        self.admins_group = Group.objects.get(name='admins')
        self.test_admin.groups.add(self.admins_group)
        self.test_admin.save()
        self.test_category = ToolCategory.objects\
            .create(title='test cat', description='test cat desc')

    def test_add_tool_get(self):
        self.client.login(username='testadmin', password='testpass')
        resp = self.client.get(reverse('tools:add'), follow=True)
        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'tools/add.html')
        self.assertContains(resp, 'Add tool')

    def test_add_tool_post(self):
        self.client.login(username='testadmin', password='testpass')
        empty = {}
        resp = self.client.post(reverse('tools:add'), empty, follow=True)
        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'tools/add.html')
        self.assertContains(resp, 'Add tool')

        test_fh = SimpleUploadedFile('test empty.png', TEST_PNG_CONTENT)
        data = {
            'title': 'our test title',
            'description': 'description test',
            'categories': self.test_category.id,
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
        self.assertTrue(self.test_category in tool.categories.all())

    def test_edit_tool_get(self):
        self.client.login(username='testadmin', password='testpass')
        tool = Tool.objects.create(
            title='A title', description='A description')

        resp = self.client.get(reverse('tools:edit', args=(tool.id,)))
        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'tools/edit.html')
        self.assertContains(resp, 'Edit tool')
        self.assertContains(resp, tool.title)
        self.assertContains(resp, tool.description)

    def test_edit_tool_post(self):
        self.client.login(username='testadmin', password='testpass')
        tool = Tool.objects.create(
            title='A title', description='A description')
        test_fh = SimpleUploadedFile('test empty.png', TEST_PNG_CONTENT)
        data = {
            'title': 'our new title',
            'description': 'new description test',
            'categories': self.test_category.id,
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
        self.assertTrue(self.test_category in tool.categories.all())

    def test_edit_tool_post_update_file(self):
        self.client.login(username='testadmin', password='testpass')
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
            'categories': self.test_category.id,
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
        self.assertTrue(tool.has_existing_cover_image())
        self.assertTrue(tool.cover_image)
        self.assertTrue(tool.cover_image.name, 'test empty2.png')
        self.assertTrue(self.test_category in tool.categories.all())

    def test_edit_tool_post_clear_cover_image(self):
        self.client.login(username='testadmin', password='testpass')
        test_fh = SimpleUploadedFile('test empty.png', TEST_PNG_CONTENT)
        tool = Tool.objects.create(
            title='A title', description='A description', cover_image=test_fh)

        data = {
            'title': 'our new title',
            'description': 'new description test',
            'categories': self.test_category.id,
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
        self.assertFalse(tool.has_existing_cover_image())
        self.assertTrue(self.test_category in tool.categories.all())

    def test_index_get(self):
        resp = self.client.get(reverse('tools:index'))
        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'tools/index.html')
        self.assertContains(resp, 'Tool overview ')

    def test_show_get(self):
        tool = Tool.objects.create(
            title='A title', description='A description')
        resp = self.client.get(reverse('tools:show', args=(tool.id, )))
        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'tools/show.html')
        self.assertContains(resp, 'Resources')
