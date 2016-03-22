import time
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_text

from tools.models import Tool
from .models import Comment


class ToolResourcesViewsTestCase(TestCase):

    def setUp(self):
        self.test_user = User.objects.create_user('testuser',
                                                  'testuser@localhost',
                                                  'testpass')
        self.test_tool = Tool.objects.create(title='test tool',
                                             description='test description')

    def test_add_comment_get_anonymous(self):
        url = reverse('comments:add')
        resp = self.client.get(url)
        print(resp.content)
        self.assertEqual(302, resp.status_code)

    def test_add_comment_get(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('comments:add')
        resp = self.client.get(url)
        print(resp.content)
        self.assertEqual(200, resp.status_code)
        #self.assertTemplateUsed(resp, 'comments/add.html')
        expected_data = {
            'ok': False,
            'errors': {},
            'comment': {},
        }
        self.assertJSONEqual(force_text(resp.content), expected_data)

    def test_add_comment_post_empty(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('comments:add')
        empty = {}
        resp = self.client.post(url, empty)
        self.assertEqual(0, Comment.objects.count())
        self.assertEqual(200, resp.status_code)
        expected_data = {
            'ok': False,
            'comment': {},
            'errors': {'content': [{'code': 'required',
                                    'message': 'This field is required.'}],
                       'related_object_id': [
                            {'code': 'required',
                             'message': 'This field is required.'}],
                       'related_object_type': [
                            {'code': 'required',
                             'message': 'This field is required.'}]}
        }
        self.assertJSONEqual(force_text(resp.content), expected_data)

    def test_add_comment_post_for_tool(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('comments:add')
        ro_type = ContentType.objects.get_for_model(self.test_tool)
        content = 'super duper comment this is yo!'
        empty = {
            'related_object_id': self.test_tool.id,
            'related_object_type': ro_type,
            'content': content
        }
        resp = self.client.post(url, empty)
        self.assertEqual(1, Comment.objects.count())
        actual = Comment.objects.all()[0]
        added_timestamp = int(time.mktime(actual.added_dt.timetuple())) * 1000
        expected_data = {
            'ok': True,
            'comment': {
                'added_dt': actual.added_dt.isoformat(),
                'author_first_name': '',
                'author_last_name': '',
                'author_username': 'testuser',
                'content': 'super duper comment this is yo!',
                'id': actual.id,
                'related_object_id': self.test_tool.id,
                'related_object_type': 'tool',
                'timestamp': added_timestamp,
            },
            'errors': {}
        }
        self.assertEqual(200, resp.status_code)
        self.assertJSONEqual(force_text(resp.content), expected_data)
        self.assertEqual(content, actual.content)
        self.assertEqual(self.test_tool.id, actual.related_object.id)
        self.assertEqual('tool', actual.related_object_type.model)
