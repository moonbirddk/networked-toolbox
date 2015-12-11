from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User, Group

from tools.models import Tool, ToolResource


TEST_PNG_CONTENT = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'


class ToolResourcesViewsTestCase(TestCase):

    def setUp(self):
        self.test_admin = User.objects.create_user('testadmin',
                                                   'testadmin@localhost',
                                                   'testpass')
        self.admins_group = Group.objects.get(name='admins')
        self.test_admin.groups.add(self.admins_group)

        self.test_tool = Tool.objects.create(title='test tool',
                                             description='test description')

        test_fh = SimpleUploadedFile('test empty.png',
                                     TEST_PNG_CONTENT)
        self.test_resource = ToolResource.objects.create(
            title='test resource',
            document=test_fh,
            content_object=self.test_tool
        )

    def test_add_resource_get(self):
        self.client.login(username='testadmin', password='testpass')
        url = reverse(
            'resources:add',
            args=('tool',self.test_tool.id,)
        )
        resp = self.client.get(url)
        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'resources/add.html')
        self.assertContains(resp, 'Add resource to')

    def test_add_resource_post_empty(self):
        self.client.login(username='testadmin', password='testpass')
        url = reverse(
            'resources:add',
            args=('tool',self.test_tool.id,)
        )
        empty = {}
        resp = self.client.post(url, empty, follow=True)
        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'resources/add.html')
        self.assertContains(resp, 'Add resource to')

    def test_add_resource_post(self):
        self.client.login(username='testadmin', password='testpass')
        url = reverse(
            'resources:add',
            args=('tool',self.test_tool.id,)
        )
        test_fh = SimpleUploadedFile(
            'test post empty.png',
            TEST_PNG_CONTENT,
            content_type='image/png'
        )
        data = {
            'title': 'test post test resource',
            'document': test_fh
        }
        resp = self.client.post(url, data, follow=True)
        self.assertEqual(200, resp.status_code)
        expected_status = (
            'http://testserver/tools/%d/' % self.test_tool.id,
            302
        )
        self.assertEqual([expected_status], resp.redirect_chain)
        self.assertTrue('messages' in resp.context)
        self.assertEqual(
            "You added a resource",
            str(list(resp.context['messages'])[0])
        )

        result = ToolResource.objects.filter(title='test post test resource',
                                             object_id=self.test_tool.id)
        self.assertEqual(1, result.count())
        tool_resource = result[0]
        self.assertEqual(tool_resource.title, data['title'])
        self.assertTrue(tool_resource.document)
        self.assertTrue(
            tool_resource.document.name,
            'test post empty.png'
        )

    def test_delete_resource_get(self):
        self.client.login(username='testadmin', password='testpass')
        url = reverse(
            'resources:delete',
            args=(self.test_resource.id,)
        )
        resp = self.client.get(url)
        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'resources/delete.html')
        self.assertContains(resp, 'Are you sure')

    def test_delete_resource_post_canceled(self):
        self.client.login(username='testadmin', password='testpass')
        url = reverse(
            'resources:delete',
            args=(self.test_resource.id,)
        )
        data = {'confirmation': 'no'}
        resp = self.client.post(url, data, follow=True)
        expected_status = (
            'http://testserver/tools/%d/' % self.test_tool.id,
            302
        )
        self.assertEqual([expected_status], resp.redirect_chain)
        actual = ToolResource.objects.filter(id=self.test_resource.id)\
            .count()
        self.assertEqual(1, actual)

    def test_delete_resource_post(self):
        self.client.login(username='testadmin', password='testpass')
        url = reverse(
            'resources:delete',
            args=(self.test_resource.id,)
        )
        data = {'confirmation': 'yes'}
        resp = self.client.post(url, data, follow=True)
        expected_status = (
            'http://testserver/tools/%d/' % self.test_tool.id,
            302
        )
        self.assertEqual([expected_status], resp.redirect_chain)
        self.assertFalse(ToolResource.objects.exists())
        self.assertTrue(Tool.objects.filter(id=self.test_tool.id)
                        .exists())
        self.assertTrue('messages' in resp.context)
        self.assertEqual(
            "You deleted a resource",
            str(list(resp.context['messages'])[0])
        )
