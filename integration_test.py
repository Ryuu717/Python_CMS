# import unittest
# from cms_app import app, db
# from cms_app.models import Content

# class TestCMSIntegrationWithDatabase(unittest.TestCase):

#     def setUp(self):
#         self.app = app.test_client()
#         self.app.testing = True
#         db.create_all()

#     def tearDown(self):
#         db.session.remove()
#         db.drop_all()

#     def test_create_content_and_database_integration(self):
#         # Test if content can be created and saved in the database
#         response = self.app.post('/create-content', data={
#             'title': 'Integration Test Post',
#             'body': 'This is a test post for integration testing.'
#         })
        
#         # Check if content is saved in the database
#         content_in_db = Content.query.filter_by(title='Integration Test Post').first()
#         self.assertIsNotNone(content_in_db)
#         self.assertEqual(content_in_db.body, 'This is a test post for integration testing.')

# if __name__ == '__main__':
#     unittest.main()
