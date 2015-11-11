from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group
from django.core.files.uploadedfile import SimpleUploadedFile

from ..models import Tool, ToolCategory

TEST_PNG_CONTENT = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'


class CategoriesViewsTestCase(TestCase):

    def setUp(self):
        self.test_admin = User.objects.create(username='testadmin')
        self.test_admin.set_password('testpass')
        self.admins_group = Group.objects.get(name='admins')
        self.test_admin.groups.add(self.admins_group)
        self.test_admin.save()

        self.test_category = ToolCategory.objects.create(
            title='test cat',
            description='test cat description'
        )
        self.test_tool = Tool.objects.create(
            title='test cat',
            description='test cat description'
        )
        self.test_tool.categories.add(self.test_category)

    def test_list_categories_get(self):
        resp = self.client.get(reverse('tools:list_categories'))
        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'tools/list_categories.html')
        self.assertContains(resp, 'Category overview')

    def test_show_category_get(self):
        url = reverse('tools:show_category', args=(self.test_category.id, ))
        resp = self.client.get(url)
        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'tools/show_category.html')
        self.assertContains(resp, self.test_category.title)

    def test_add_category_get(self):
        self.client.login(username='testadmin', password='testpass')
        resp = self.client.get(reverse('tools:add_category'))
        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'tools/add_category.html')
        self.assertContains(resp, 'Add category')

    def test_add_category_post(self):
        self.client.login(username='testadmin', password='testpass')
        empty = {}
        resp = self.client.post(
            reverse('tools:add_category'), empty, follow=True)
        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'tools/add_category.html')
        self.assertContains(resp, 'Add category')

        test_fh = SimpleUploadedFile('test empty.png', TEST_PNG_CONTENT)
        data = {
            'title': 'our test title',
            'description': 'description test',
            'cover_image': test_fh
        }
        resp = self.client.post(reverse('tools:add_category'), data,
                                follow=True)

        actual = ToolCategory.objects.filter(title=data['title'])
        self.assertEqual(actual.count(), 1)
        category = actual[0]

        self.assertEqual(category.title, data['title'])
        self.assertEqual(category.description, data['description'])
        self.assertTrue(category.cover_image)
        self.assertTrue(category.cover_image.name, 'test empty.png')

        expected_url = 'http://testserver/tools/categories/show/{}/'.format(
            category.id)
        self.assertEqual(
            [(expected_url, 302)], resp.redirect_chain)
        self.assertTrue('messages' in resp.context)
        self.assertEqual(
            "You created a category", str(list(resp.context['messages'])[0]))

    def test_edit_category_get(self):
        self.client.login(username='testadmin', password='testpass')
        resp = self.client.get(reverse('tools:edit_category',
                                       args=(self.test_category.id,)))
        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'tools/edit_category.html')
        self.assertContains(resp, 'Edit category')
        self.assertContains(resp, self.test_category.title)
        self.assertContains(resp, self.test_category.description)

    def test_edit_category_post(self):
        self.client.login(username='testadmin', password='testpass')
        test_fh = SimpleUploadedFile('test empty.png', TEST_PNG_CONTENT)
        data = {
            'title': 'our category new title',
            'description': 'new category description test',
            'cover_image': test_fh,
        }
        url = reverse('tools:edit_category', args=(self.test_category.id,))
        resp = self.client.post(url, data, follow=True)
        self.assertTrue('messages' in resp.context)
        self.assertEqual(
            "You updated this category", str(list(resp.context['messages'])[0]))
        self.assertContains(resp, data['title'])
        category = ToolCategory.objects.get(id=self.test_category.id)
        self.assertTrue(category.cover_image)
        self.assertTrue(category.cover_image.name, 'test empty.png')
        self.assertEqual(
            [('http://testserver/tools/categories/show/%d/' % category.id, 302)],
            resp.redirect_chain)

    def test_delete_category_get(self):
        self.client.login(username='testadmin', password='testpass')
        url = reverse(
            'tools:delete_category',
            args=(self.test_category.id, )
        )
        resp = self.client.get(url)
        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'tools/delete_category.html')
        self.assertContains(resp, 'Are you sure')

    def test_delete_category_post(self):
        self.client.login(username='testadmin', password='testpass')
        url = reverse(
            'tools:delete_category',
            args=(self.test_category.id, )
        )
        data = {'confirmation': 'yes'}
        resp = self.client.post(url, data, follow=True)
        expected_status = (
            'http://testserver/tools/categories/',
            302
        )
        self.assertEqual([expected_status], resp.redirect_chain)
        self.assertFalse(ToolCategory.objects.exists())
        self.assertTrue(Tool.objects.filter(id=self.test_tool.id)
                        .exists())
        expected_tool_categories = Tool.objects.get(id=self.test_tool.id)\
            .categories.all().count()
        self.assertEqual(0, expected_tool_categories)
        self.assertTrue('messages' in resp.context)
        self.assertEqual(
            "You deleted a category",
            str(list(resp.context['messages'])[0])
        )
