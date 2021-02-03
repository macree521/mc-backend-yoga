from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow 
from flask_cors import CORS
import os

app = Flask(__name__)
cors = CORS(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    questionText = db.Column(db.String(30), unique=False)
    answerText1 = db.Column(db.String(35), nullable=False)
    answerText2 = db.Column(db.String(35), nullable=False)
    answerText3 = db.Column(db.String(35), nullable=False)
    answerText4 = db.Column(db.String(35), nullable=False)

    def __init__(self, questionText, answerText1, answerText2, answerText3, answerText4):
        self.questionText = questionText
        self.answerText1 = answerText1
        self.answerText2 = answerText2
        self.answerText3 = answerText3
        self.answerText4 = answerText4

class QuestionSchema(ma.Schema):
    class Meta:
        fields = ('questionText', 'answerText1', 'answerText2', 'answerText3', 'answerText4')

question_schema = QuestionSchema()
questions_schema = QuestionSchema(many=True)

# Endpoint to create a new question
@app.route('/question', methods=["POST"])
def add_question():
    questionText = request.json['questionText']
    answerText1 = request.json['answerText1']
    answerText2 = request.json['answerText2']
    answerText3 = request.json['answerText3']
    answerText4 = request.json['answerText4']

    new_question = Question(questionText, answerText1, answerText2, answerText3, answerText4)

    db.session.add(new_question)
    db.session.commit()

    question = Question.query.get(new_question.id)

    return question_schema.jsonify(question)

# Endpoint to query all questions
@app.route('/questions', methods=["GET"])
def get_questions():
    all_questions = Question.query.all()
    result = questions_schema.dump(all_questions)
    return jsonify(result)

# Endpoint for querying a single question
@app.route('/question/<id>', methods=["GET"])
def get_question(id):
    question = Question.query.get(id)
    return question_schema.jsonify(question)

#Endpoint for updating a question
@app.route('/question/<id>', methods=["PUT"])
def update_question(id):
    question = Question.query.get(id)
    questionText = request.json['questionText']
    answerText1 = request.json['answerText1']
    answerText2 = request.json['answerText2']
    answerText3 = request.json['answerText3']
    answerText4 = request.json['answerText4']

    question.questionText = questionText
    question.answerText1 = answerText1
    question.answerText2 = answerText2
    question.answerText3 = answerText3
    question.answerText4 = answerText4

    db.session.commit()
    return question_schema.jsonify(question)

#Endpoint for deleting a record
@app.route('/question/<id>', methods=["DELETE"])
def delete_question(id):
    question = Question.query.get(id)
    db.session.delete(question)
    db.session.commit()

    return "Question was successfully deleted"

if __name__ == '__main__':
    app.run(debug=True)