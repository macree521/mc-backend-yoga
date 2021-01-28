from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow 
import os

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)