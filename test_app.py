import unittest
from app import app

class BasicTestCase(unittest.TestCase):
    def test_index(self):
        tester = app.test_client(self)
        pages = ['/']
        for page in pages:
            response = tester.get(page, content_type='html/text')
            self.assertEqual(response.status_code, 200)
    def test_other(self):
        tester = app.test_client(self)
        response = tester.get('test', content_type='html/text')
        self.assertEqual(response.status_code, 404)

    def test_api(self):
        url = '/health'
        tester = app.test_client(self)
        response = tester.get(url)
        self.assertEqual(response.get_data(),b'ok')
        self.assertEqual(response.status_code,200)

if __name__ == '__main__':
    unittest.main() 