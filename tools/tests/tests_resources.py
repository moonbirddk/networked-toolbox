from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from tools.models import Tool, ToolResource
from tools.utils import generate_upload_path


TEST_PNG_CONTENT = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'

class ResourcesViewsTestCase(TestCase):

    def setUp(self):
        self.test_tool = Tool.objects.create(title='test tool',
            description='test description')


    def test_add_resource_get(self):
        url = reverse(
            'tools:add_resource',
            args=(self.test_tool.id,)
        )
        resp = self.client.get(url)
        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'tools/add_resource.html')
        self.assertContains(resp, 'Add resource to')

    def test_add_resource_post(self):
        url = reverse(
            'tools:add_resource',
            args=(self.test_tool.id,)
        )
        empty = {}
        resp = self.client.post(url, empty, follow=True)
        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'tools/add_resource.html')
        self.assertContains(resp, 'Add resource to')

        test_fh = SimpleUploadedFile('test empty.png',
            TEST_PNG_CONTENT)
        data = {
            'title': 'our test resouce',
            'document': test_fh
        }

        resp = self.client.post(url, data, follow=True)
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

        self.assertEqual(ToolResource.objects.count(), 1)
        tool_resource = ToolResource.objects.all()[0]
        self.assertEqual(tool_resource.title, data['title'])
        self.assertTrue(tool_resource.document)
        self.assertTrue(
            tool_resource.document.name,
            'test empty.png'
        )
