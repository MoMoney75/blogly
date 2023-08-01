from app import app
from flask import Flask
from models import db, User, Post, Tag, create_timestamp
import unittest


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users'
app.config['WTF_CSRF_ENABLED'] = False  # no CSRF during tests
app.config["TESTING"] = True




class test_app(unittest.TestCase):
    def setUp(self):
        """Stuff to do before every test"""
        
        self.client = app.test_client()
        """CREATING INSTANCE OF USER FOR TESTING PURPOSES"""
        #Test_User = User(first_name="Test", last_name="User", image_url='www.clown.com')
        #db.session.add(Test_User)
        #db.session.commit()

    def tearDown(self):
        db.session.rollback()

#################TESTING HOME PAGE AND USERS ROUTES########################
    def test_home_page(self):
        with app.test_client() as client:
            response = self.client.get('/', follow_redirects=True)
            htmlresponse = response.get_data(as_text=True)
            """TESTING HOME PAGE TO SEE IF IT LOADS"""
            self.assertEqual(response.status_code,200)
            self.assertIn('<h1>Welcome to Blogly!</h1>',htmlresponse)

            """TESTING HOME PAGE TO SEE IF LIST OF USERS IS SHOWN"""
            self.assertIn('Test User', htmlresponse)

    def test_render_newUser_form(self):
        with app.test_client() as client:
            """TESTING TO SEE IF CREATE USER FORM IS RENDERED"""
            response = self.client.get('/new_user_form', follow_redirects=True)
            htmlresponse = response.get_data(as_text=True)

           
            self.assertEqual(response.status_code,200)
            self.assertIn('<h2 id="newUserH2">Create a new user:</h2>', htmlresponse)

    def test_handle_newUser(self):
        """TESTING SUBMITTING NEW USER FORM"""
        with app.test_client() as client:
            data ={'first_name': 'Test', 'last_name' :'User2', 'image_url': 'www.clown.com' }
            response = self.client.post('/new_user_handle', data=data, follow_redirects=True)
            html = response.get_data(as_text=True)

            """NEWLY CREATED USER SHOULD BE ON LIST OF ALL USERS WHEN REDIRECTED TO HOME PAGE"""
            self.assertEqual(response.status_code, 200)
            self.assertIn('Test User2', html)


##########################TESTING POSTING_BLOG ROUTES######################


    def test_create_post(self):
        """TESTING CREATING A NEW POST"""
        with app.test_client() as client:
            
            data = {'title':'TEST TITLE', 'content': 'TEST CONTENT', 'created_at': create_timestamp()}
            response = self.client.post('/1/new_post', data=data, follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code,200)
            self.assertIn('TEST TITLE', html)



    def test_all_posts(self):
        """TESTING GETTING ALL BLOGS"""
        with app.test_client() as client:
            response = self.client.get('/all_blogs')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<h1>All Current Blogs:</h1>',html)

##########################TESTING TAG ROUTES ##############################

    def test_render_tagForm(self):
        """TESTING CREATING TAGS FOR POSTS"""
        with app.test_client() as client:
            response = self.client.get('/create_tag')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<input type="text" name="name" id="create_tag">',html)

    def test_create_tag(self):
        """TESTING SUBMISSION OF CREATING A TAG"""
        with app.test_client() as client:
            data = {'name':'TEST TAG'}
            response = self.client.post('/create_tag', data=data, follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('TEST TAG', html)







