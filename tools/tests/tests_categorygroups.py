from django.conf import settings
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core import mail
from django.contrib.auth.models import User, Group

from ..models import ToolCategory, CategoryGroup, Tool


class CategoryGroupModelTestCase(TestCase):
    """
    Tests for CategoryGroup model. Some of it may look like testing DJ API
    but I decided to add it because of convoluted logic in User Stories.
    """

    def setUp(self):
        self.test_admin = User.objects.create(username='testadmin')
        self.test_admin.set_password('testpass')
        self.admins_group = Group.objects.get(name='admins')
        self.test_admin.groups.add(self.admins_group)
        self.test_admin.save()

    def test_default_category_group(self):
        test_cat = ToolCategory.objects.create(
            title="test cat",
            description="desc",
            published=True
        )
        self.assertEqual(1, CategoryGroup.objects.all().count())
        default_group = CategoryGroup.objects.all()[0]
        self.assertEqual(1, default_group.id)
        self.assertEqual("Other", default_group.name)
        self.assertEqual(test_cat.group, default_group)

    def test_delete_group(self):
        default_group = CategoryGroup.objects.get(name="Other")
        test_group = CategoryGroup.objects.create(name="a new group")
        test_cat = ToolCategory.objects.create(
            title="test cat",
            description="desc",
            published=True,
            group=test_group
        )
        self.assertEqual(test_cat.group, test_group)
        test_group.delete()
        test_cat = ToolCategory.objects.get(id=test_cat.id)
        self.assertEqual(test_cat.group, default_group)

    def test_delete_category(self):
        test_group = CategoryGroup.objects.create(name="a new group")
        test_cat = ToolCategory.objects.create(
            title="test cat",
            description="desc",
            published=True,
            group=test_group
        )
        test_cat2 = ToolCategory.objects.create(
            title="test cat2",
            description="desc2",
            published=True,
            group=test_group
        )
        test_tool = Tool.objects.create(
            title="tool name",
            description="a desc",
            published=True
        )

        test_cat.delete()
        self.assertTrue(CategoryGroup.objects.filter(name="a new group")
                        .exists())

        test_group.delete()
        self.assertTrue(ToolCategory.objects.filter(id=test_cat2.id)
                        .exists())


class CategoryGroupViewsTestCase(TestCase):
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

    def test_add_categorygroup_get(self):
        self.client.login(username='testadmin', password='testpass')
        url = reverse('tools:add_categorygroup')
        resp = self.client.get(url)
        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'tools/add_categorygroup.html')

    def test_add_categorygroup_post(self):
        self.client.login(username='testadmin', password='testpass')
        url = reverse('tools:add_categorygroup')
        data = {
            'name': 'some group name',
            'categories': [self.test_category.id, ]
        }
        resp = self.client.post(url, data, follow=True)
        self.assertEqual(
            [('http://testserver/tools/categories/', 302)], resp.redirect_chain)
        self.assertTrue('messages' in resp.context)
        self.assertEqual(
            "You have added the category group",
            str(list(resp.context['messages'])[0]))

    def test_edit_categorygroup_get(self):
        self.client.login(username='testadmin', password='testpass')
        test_group = CategoryGroup.objects.create(name='test group')
        url = reverse('tools:edit_categorygroup', args=(test_group.id, ))
        resp = self.client.get(url)
        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'tools/edit_categorygroup.html')

    def test_edit_categorygroup_post(self):
        self.client.login(username='testadmin', password='testpass')
        test_group = CategoryGroup.objects.create(name='test group')
        url = reverse('tools:edit_categorygroup', args=(test_group.id, ))
        data = {
            'name': 'new group name',
            'categories': [self.test_category.id, ]
        }
        resp = self.client.post(url, data, follow=True)
        self.assertEqual(
            [('http://testserver/tools/categories/', 302)], resp.redirect_chain)
        self.assertTrue('messages' in resp.context)
        self.assertEqual(
            "You have updated the category group", str(list(resp.context['messages'])[0]))

    def test_delete_categorygroup_get(self):
        self.client.login(username='testadmin', password='testpass')
        test_group = CategoryGroup.objects.create(name='test group')
        url = reverse('tools:delete_categorygroup', args=(test_group.id, ))
        resp = self.client.get(url)
        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'tools/delete_categorygroup.html')

    def test_delete_categorygroup_post(self):
        self.client.login(username='testadmin', password='testpass')
        test_group = CategoryGroup.objects.create(name='test group')
        url = reverse('tools:delete_categorygroup', args=(test_group.id, ))
        data = {
            'confirmation': 'yes',
        }
        resp = self.client.post(url, data, follow=True)
        self.assertEqual(
            [('http://testserver/tools/categories/', 302)], resp.redirect_chain)
        self.assertTrue('messages' in resp.context)
        self.assertEqual(
            "You have deleted the category group", str(list(resp.context['messages'])[0]))
