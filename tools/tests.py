from django.test import TestCase

# Create your tests here.

class HomeViewTestCase(TestCase):
    def test_home_get(self):
        resp = self.client.get('/')
        self.assertEqual(200, resp.status_code)

class ToolsViewsTestCase(TestCase):
    def setUp(self):
        pass

    def test_add_tool_get(self):
        resp = self.client.get('/tools/add/')
        self.assertEqual(200, resp.status_code)

    def test_add_tool_post(self):
        data = {
            'title': 'our test title',
            'description': 'description test',
        }
        resp = self.client.post('/tools/add/', data, follow=True)
        self.assertEqual([('http://testserver/', 302)], resp.redirect_chain)
        self.assertTrue('messages' in resp.context)
        self.assertEqual("You created a tool", str(list(resp.context['messages'])[0]))

