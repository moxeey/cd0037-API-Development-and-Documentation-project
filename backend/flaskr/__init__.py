import json
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)   

    """
    @DONE: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={r"/*": {"origins": "*"}})
    # CORS(app)
    """
    @DONE: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    """
    @DONE:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def get_categories():
        try:
            categories = Category.query.all()
            formatted_categories={}
            for cat in categories:
                formatted_categories[cat.id] = cat.type        
                
            return jsonify({'success':True, 'categories':formatted_categories})
        except:
            abort(422)
    """
    @DONE:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions')
    def get_questions():
        page = request.args.get(key='page', default=1, type=int)
        start = (page-1)*QUESTIONS_PER_PAGE
        end = (start+QUESTIONS_PER_PAGE)
        
        try:
            categories = Category.query.all()
        
            formatted_categories={}
            for cat in categories:
                formatted_categories[cat.id] = cat.type        
            
            questions = Question.query.all()
            formatted_questions = [question.format() for question in questions]

            return jsonify({
                'success':True,
                'questions': formatted_questions[start:end],
                'total_questions': len(formatted_questions),
                'current_category': formatted_categories[1],
                'categories': formatted_categories
                
            })
        except:
            abort(422)
    """
    @DONE:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.filter(Question.id == question_id).one_or_none()
        if question is None:
            abort(404)
        try:
            question.delete()
            return jsonify({
                'success': True,
                'deleted_question': question.format()
            })
        except:
            abort(422)

    """
    @DONE:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def add_question():
        try:
            data = request.get_json()
            question = Question(
                question=data['question'],
                answer=data['answer'],
                category=data['category'],
                difficulty=data['difficulty']
                )
            question.insert()
            
            return jsonify({
                'success':True,
                'question': question.format()
            })
        except: 
            abort(422)

    """
    @DONE:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions/search', methods=['POST'])
    def search_question():
        try:
            data = request.get_json()
            searchTerm = data.get('searchTerm')
            questions = Question.query.filter(Question.question.ilike(f'%{searchTerm}%'))
            return jsonify({
                'success':True,
                'questions': [question.format() for question in questions]
            })
        except:
            abort(422)

    """
    @DONE:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<category_id>/questions')
    def get_category_questions(category_id):
        page = request.args.get(key='page', default=1, type=int)
        start = (page-1)*QUESTIONS_PER_PAGE
        end = (start+QUESTIONS_PER_PAGE)
        
        category = Category.query.filter(Category.id == category_id).one_or_none()
            
        if category is None:
            abort(404)
        try:
            questions = Question.query.filter(Question.category == category_id).all()
            formated_questions = [question.format() for question in questions]
            return jsonify({    
                'success':True,
                'questions': formated_questions[start:end],
                'total_questions': len(formated_questions),
                'current_category': Category.query.get(category_id).format()['type'],                
            })
        except:
            abort(422)
    """
    @DONE:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def get_quiz_question():
        data = request.get_json()
        try:
            category = data['quiz_category']
            prev_questions = data['previous_questions']
            
            questions = []
            if not category['id']:
                questions = Question.query.filter((~Question.id.in_(prev_questions))).all()
               
            else:
                questions = Question.query.filter(Question.category == category['id'] ,(~Question.id.in_(prev_questions))).all()

            question = random.choice(questions).format() if len(questions)> 0 else None  
            return jsonify({
                'success':True,
                'question': question
            })
        except:
            abort(422)
        
    """
    @DONE:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success':False,
            'message':'Resouce not found',
            'error': 404,
        }),404
    @app.errorhandler(422)
    def unprocessed(error):
        return jsonify({
            'success':False,
            'message':'Unprocessed',
            'error': 422,
        }),422
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success':False,
            'message':'Bad request',
            'error': 400,
        }),400
    @app.errorhandler(500)
    def server_error(error):    
        return jsonify({
            'success':False,
            'message':'Server error',
            'error': 500,
        }),500
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success':False,
            'message':'Method not allowed',
            'error': 405,
        }),405
    
        
    return app

