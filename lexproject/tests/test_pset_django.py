from django.test import TestCase, Client


class TestCaseLex(TestCase):

    def test_get_on_index(self):
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_post_on_index(self):
        client = Client()
        data = {"CheckIn": "COVID-19", "CheckOut": "5" }
        response= client.post('/', data)
        self.assertEqual(response.status_code, 200)


