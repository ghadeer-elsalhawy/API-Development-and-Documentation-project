import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

# Implement pagination to get data per page


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in selection]
    current_questions = questions[start:end]
    return current_questions

    # Done


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={r"*/api/*": {"origins": "*"}})

    # Done

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    # Done

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    # View all availabe categories
    @app.route('/categories', methods=['GET'])
    def show_categories():
        categories = Category.query.all()
        # Handle error
        if len(categories) == 0:
            abort(404)

        categoriesDict = {}
        for c in categories:
            categoriesDict[c.id] = c.type
        # print(categoriesDict)
        return jsonify({
            'success': True,
            'categories': categoriesDict})

    # Done

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    # Get 10 paginated questions, total questions, all categories, and current category
    @app.route('/questions', methods=['GET'])
    def view_questions():
        selection = Question.query.all()
        questionsShowed = paginate_questions(request, selection)
        if len(questionsShowed) == 0:
            abort(404)

        categories = Category.query.all()
        categoriesDict = {}
        for c in categories:
            categoriesDict[c.id] = c.type

        return jsonify({
            'success': True,
            'questions': questionsShowed,
            'totalQuestions': len(selection),
            'categories': categoriesDict,
            'currentCategory': None
        })

        # Done

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        try:
            wantedQuestion = Question.query.filter_by(id=id).one_or_none()
            if wantedQuestion == None:
                abort(404)
            wantedQuestion.delete()
            return jsonify({'success': True})
        except:
            abort(422)

    # Done

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    @app.route('/questions', methods=['POST'])
    def add_question():
        addedQuestion = request.get_json()
        q = addedQuestion.get('question')
        ans = addedQuestion.get('answer')
        dif = addedQuestion.get('difficulty')
        cat = addedQuestion.get('category')
        if (addedQuestion, q, ans, dif, cat) == None:
            abort(422)
        try:
            new_question = Question(
                question=q, answer=ans, difficulty=dif, category=cat)
            new_question.insert()
            selection = Question.query.all()
            allQuestions = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'totalQuestions': len(allQuestions),
                'questions': allQuestions
            })
        except:
            abort(422)

    # Done

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    @app.route("/search", methods=['POST'])
    def search_question():
        term = request.args.get('search')
        selection = Question.query.filter(
            Question.question.ilike(f'%{term}%')).all()
        search_questions = paginate_questions(request, selection)
        if term is None:
            abort(404)

        return jsonify({
            'success': True,
            'questions': list(search_questions),
            'totalQuestions': len(selection),
            'currentCategory': None
        })

    # Done

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    return app
