from django.conf import settings
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core import mail
from django.contrib.auth.models import User, Group

from ..models import ToolOverviewPage, CategoryOverviewPage


class OverviewTestCase(TestCase):

    def setUp(self):
        self.test_admin = User.objects.create(username='testadmin')
        self.test_admin.set_password('testpass')
        self.admins_group = Group.objects.get(name='admins')
        self.test_admin.groups.add(self.admins_group)
        self.test_admin.save()

    def test_edit_overview_get(self):
        self.client.login(username='testadmin', password='testpass')

        url = reverse('tools:edit_overview', args=('tool',))
        resp = self.client.get(url)
        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'tools/edit_overview.html')

        url = reverse('tools:edit_overview', args=('category',))
        resp = self.client.get(url)
        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'tools/edit_overview.html')

        url = reverse('tools:edit_overview', args=('other',))
        resp = self.client.get(url)
        self.assertEqual(404, resp.status_code)

    def test_edit_overview_post_tool(self):
        self.client.login(username='testadmin', password='testpass')

        url = reverse('tools:edit_overview', args=('tool',))
        data = {'description': 'some desc1'}
        resp = self.client.post(url, data, follow=True)
        expected_url = 'http://testserver/tools/'
        self.assertEqual(
            [(expected_url, 302)], resp.redirect_chain)
        self.assertTrue('messages' in resp.context)
        self.assertEqual(
            "You have changed the overview page.",
            str(list(resp.context['messages'])[0]))

    def test_edit_overview_post_category(self):
        self.client.login(username='testadmin', password='testpass')

        url = reverse('tools:edit_overview', args=('category',))
        data = {'description': 'some desc1'}
        resp = self.client.post(url, data, follow=True)
        expected_url = 'http://testserver/tools/categories/'
        self.assertEqual(
            [(expected_url, 302)], resp.redirect_chain)
        self.assertTrue('messages' in resp.context)
        self.assertEqual(
            "You have changed the overview page.",
            str(list(resp.context['messages'])[0]))
