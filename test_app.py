from app import app
import unittest


class AppTestCase(unittest.TestCase):
    def setUp(self):
        """Stuff to do before every test"""
        self.client = app.test_client()
        app.config['TESTING'] = True

#class test_home_page(TestCase):


    def test_home_page(self):
        with app.test_client() as client:
            response = self.client.get('/', follow_redirects=True)
            htmlresponse = response.get_data(as_text=True)

            self.assertEqual(response.status_code,200)
            self.assertIn('<h1>Welcome to Blogly!</h1>',htmlresponse)

    def test_create_post(self):
        with app.test_client as client:
            response= self.client.get('/<int:user_id>/new_post')
            

