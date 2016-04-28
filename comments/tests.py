from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_text

from tools.models import Tool
from .models import ThreadedComment
from .utils import format_added_dt
from .templatetags.commentstags import CommentListNode


class ToolCommentsViewsTestCase(TestCase):
    maxDiff = None

    def setUp(self):
        self.test_user = User.objects.create_user('testuser',
                                                  'testuser@localhost',
                                                  'testpass')
        self.test_tool = Tool.objects.create(title='test tool',
                                             description='test description')

        self.test_user.profile.country = 'PL'
        self.test_user.profile.save()

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
        self.assertEqual(0, ThreadedComment.objects.count())
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
        self.assertEqual(1, ThreadedComment.objects.count())
        actual = ThreadedComment.objects.all()[0]
        expected_data = {
            'ok': True,
            'comment': {
                'added_dt': actual.added_dt.isoformat(),
                'added_time': format_added_dt(actual.added_dt),
                'author_country_code': 'PL',
                'author_country_name': 'Poland',
                'author_url': '/profiles/{}/'.format(self.test_user.profile.uid),
                'author_name': 'Noname Nosurname',
                'author_photo_url': '/static/profiles/images/Small%20user%20pic.png',
                'content': content,
                'id': actual.id,
                'tree_id': actual.id,
                'parent_id': None,
                'related_object_id': self.test_tool.id,
                'related_object_type': 'tool',
            },
            'errors': {}
        }
        self.assertEqual(200, resp.status_code)
        self.assertJSONEqual(force_text(resp.content), expected_data)
        self.assertEqual(content, actual.content)
        self.assertEqual(self.test_tool.id, actual.related_object.id)
        self.assertEqual('tool', actual.related_object_type.model)

    def test_add_comment_reply_post_for_tool(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('comments:add')
        ro_type = ContentType.objects.get_for_model(self.test_tool)

        test_parent = ThreadedComment.objects.create(
            author=self.test_user,
            content='1111 parent',
            related_object=self.test_tool,
        )
        test_parent.tree_id = test_parent.id
        test_parent.save()

        content = '2222 child'
        empty = {
            'related_object_id': self.test_tool.id,
            'related_object_type': ro_type,
            'content': content,
            'parent': test_parent.id,
        }
        resp = self.client.post(url, empty)
        self.assertEqual(2, ThreadedComment.objects.count())
        actual = ThreadedComment.objects.all().order_by('tree_id', 'added_dt')[1]
        expected_data = {
            'ok': True,
            'comment': {
                'added_dt': actual.added_dt.isoformat(),
                'added_time': format_added_dt(actual.added_dt),
                'author_country_code': 'PL',
                'author_country_name': 'Poland',
                'author_url': '/profiles/{}/'.format(self.test_user.profile.uid),
                'author_name': 'Noname Nosurname',
                'author_photo_url': '/static/profiles/images/Small%20user%20pic.png',
                'content': content,
                'id': actual.id,
                'parent_id': test_parent.id,
                'related_object_id': self.test_tool.id,
                'related_object_type': 'tool',
                'tree_id': test_parent.id,
            },
            'errors': {}
        }
        self.assertEqual(200, resp.status_code)
        self.assertJSONEqual(force_text(resp.content), expected_data)
        self.assertEqual(content, actual.content)
        self.assertEqual(self.test_tool.id, actual.related_object.id)
        self.assertEqual('tool', actual.related_object_type.model)

        expected = {}
        expected[test_parent.id] = {
            'parent': test_parent,
            'replies': [actual],
        }
        comments_dict = CommentListNode\
            .get_comments_dict(qs=ThreadedComment.objects.all())
        self.assertDictEqual(expected, comments_dict)

    def test_add_comment_post_for_tool_with_tags(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('comments:add')
        ro_type = ContentType.objects.get_for_model(self.test_tool)
        content = 'super <a href="kk.dk">kk.dk</a>comment this is yo!'
        empty = {
            'related_object_id': self.test_tool.id,
            'related_object_type': ro_type,
            'content': content
        }
        resp = self.client.post(url, empty)
        self.assertEqual(1, ThreadedComment.objects.count())
        actual = ThreadedComment.objects.all()[0]
        expected_data = {
            'comment': {
                'added_dt': actual.added_dt.isoformat(),
                'added_time': format_added_dt(actual.added_dt),
                'author_country_name': 'Poland',
                'author_country_code': 'PL',
                'author_name': 'Noname Nosurname',
                'author_url': '/profiles/{}/'.format(self.test_user.profile.uid),
                'author_photo_url': '/static/profiles/images/Small%20user%20pic.png',
                'content': 'super kk.dkcomment this is yo!',
                'id': actual.id,
                'tree_id': actual.id,
                'parent_id': None,
                'related_object_id': self.test_tool.id,
                'related_object_type': 'tool'
            },
                'errors': {},
                'ok': True
        }
        self.assertEqual(200, resp.status_code)
        self.assertJSONEqual(force_text(resp.content), expected_data)
