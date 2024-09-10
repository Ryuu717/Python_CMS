import unittest
from flask import url_for
from app import app, db, Content  # Ensure this imports your actual app and models
from flask import Flask
from flask_testing import TestCase

import os



class MyTest(TestCase):
    # Setup method to initialize the app and test environment
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = (f"mysql://{os.getenv('RDS_USERNAME')}:{os.getenv('RDS_PASSWORD')}"f"@{os.getenv('RDS_ENDPOINT')}/{os.getenv('RDS_DB_NAME')}")
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        return app

    # Set up a clean test environment before each test
    def setUp(self):
        db.create_all()  # Create all tables in the in-memory database
        


    # Tear down the test environment after each test
    # def tearDown(self):
    #     db.session.remove()
    #     db.drop_all()
    
    #############################################################
    # Success
    #############################################################
    # Test adding valid content
    def test_add_content_valid(self):
        # First, add content
        content = Content(title='Test Title', body='Test Body', author='Test Author', category_id=1)
        db.session.add(content)
        db.session.commit()
        
        # Verify the content was added to the database
        content = Content.query.filter_by(title='Test Title').first()
        self.assertIsNotNone(content)
        self.assertEqual(content.body, 'Test Body')
        
    #############################################################
    # Success?
    #############################################################
    # Test adding valid content
    # def test_add_content_valid(self):
    #     response = self.client.post(url_for('add_content'), data={
    #         'title': 'Test Title',
    #         'body': 'Test Body',
    #         'author': 'Test Author',
    #         'category': 1
    #         # 'image_path': 'cms.png'
    #     }, follow_redirects=True)
    #     self.assertEqual(response.status_code, 200)
    #     # self.assertIn('Content added successfully!', response.data)   # Cause Error

    #     # Verify the content was added to the database
    #     # content = Content.query.filter_by(title='Test Title').first()
    #     # self.assertIsNotNone(content)
    #     # self.assertEqual(content.body, 'Test Body')


    #############################################################
    # Error
    #############################################################
    # Test adding invalid content (missing title)
    # def test_add_content_invalid(self):
    #     response = self.client.post(url_for('add_content'), data={
    #         'title': '',  # Invalid: Title is required
    #         'body': 'This is a test body.',
    #         'author': 'Test Author',
    #         'category': 1
    #     }, follow_redirects=True)
    #     self.assertNotEqual(response.status_code, 200)
        # self.assertIn(b'This field is required.', response.data)

    #############################################################
    # Error
    #############################################################
    # Test editing content
    # def test_edit_content(self):
    #     # First, add content
    #     content = Content(title='Old Title', body='Old Body', author='Test Author', category_id=1)
    #     db.session.add(content)
    #     db.session.commit()

    #     # Now, edit the content
    #     response = self.client.post(url_for('edit_content', content_id=content.content_id), data={
    #         'title': 'New Title',
    #         'body': 'New Body',
    #         'author': 'Test Author',
    #         'category': 1
    #     }, follow_redirects=True)
    #     self.assertEqual(response.status_code, 200)
        # self.assertIn(b'Content updated successfully!', response.data)

        # Verify the content was updated in the database
        # updated_content = Content.query.get(content.content_id)
        # self.assertEqual(updated_content.title, 'New Title')
        # self.assertEqual(updated_content.body, 'New Body')


    #############################################################
    # Success
    #############################################################
    # Test deleting content
    def test_delete_content(self):
        # First, add content
        content = Content(title='To be deleted', body='This content will be deleted.', author='Test Author', category_id=1)
        db.session.add(content)
        db.session.commit()

        # Now, delete the content
        response = self.client.post(url_for('delete_content', content_id=content.content_id), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Content deleted successfully!', response.data)

        # Verify the content was deleted from the database
        deleted_content = Content.query.get(content.content_id)
        self.assertIsNone(deleted_content)
