import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from models import setup_db, Question, Category
from settings import DB_TEST_NAME, DB_USER, DB_PASSWORD

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = DB_TEST_NAME
        self.database_path = "postgresql://{}:{}@{}/{}".format(DB_USER, DB_PASSWORD,'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    
    """
    TEST GET /categories
    """
    def test_get_categories(self):
        res = self.client().get('/categories')
        self.assertEqual(res.status_code, 200)

    def test_get_categories_error(self):
        res = self.client().delete('/categories')
        self.assertEqual(res.status_code, 405)

    """
    TEST GET /questions
    """
    def test_get_questions(self):
            res = self.client().get('/questions')
            self.assertEqual(res.status_code, 200)

    def test_get_questions_error(self):
            res = self.client().put('/questions')
            self.assertEqual(res.status_code, 405)

    """
    TEST DELETE /questions/<question_id>
    """
    def test_delete_question(self):
            res = self.client().delete('/questions/6')
            question = Question.query.filter(Question.id == 5).one_or_none()
            
            self.assertEqual(question, None)
            self.assertEqual(res.status_code, 200)

    def test_delete_question_error(self):
            res = self.client().delete('/questions/99')
            self.assertEqual(res.status_code, 404)

    """
    TEST POST /questions
    """
    def test_add_question(self):
        res = self.client().post('/questions', json={
            "answer": "Agra",
            "category": 3,
            "difficulty": 2,
            "question": "The Taj Mahal is located in which Indian city?"
        })
        self.assertEqual(res.status_code, 200)
    
    def test_add_question_error(self):
        res = self.client().post('/questions/2', json={
            "answer": "Agra",
            "category": 3,
            "difficulty": 2,
            "question": "The Taj Mahal is located in which Indian city?"
        })
        self.assertEqual(res.status_code, 405)

    """
    TEST POST /questions/search
    """
    def test_search_questions(self):
            res = self.client().post('/questions/search', json={'searchTerm':'World'})
            self.assertEqual(res.status_code, 200)

    def test_search_question_error(self):
            res = self.client().post('/questions/search')
            self.assertEqual(res.status_code, 422)

    """
    TEST GET categories/<category_id>/questions
    """    
    def test_get_category_questions(self):
        res = self.client().get('categories/1/questions')
        self.assertEqual(res.status_code, 200)

    def test_get_category_questions_error(self):
            res = self.client().get('categories/100/questions')
            self.assertEqual(res.status_code, 404)
    
    """
    TEST POST /quizzes
    """    
    def test_generate_quizzes(self):
        res = self.client().post('/quizzes', json={
            "previous_questions": [1,2,3],
            "quiz_category": {"id":2,"type": "Art"}
        })
        self.assertEqual(res.status_code, 200)
    
    def test_generate_quizzes_error(self):
        res = self.client().post('/quizzes')
        self.assertEqual(res.status_code, 422)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()