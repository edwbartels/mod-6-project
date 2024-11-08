from flask import Blueprint,jsonify,request
from flask_login import current_user
from ..models.question import Question
from ..models.vote import Vote
from ..models.comment import Comment
from ..models.answer import Answer
from ..models.db import db
from ..utils.decorator import login_check

bp = Blueprint("vote", __name__, url_prefix="/api")


@bp.route('/vote', methods=['POST'])
@login_check
def add_vote():
    data = request.get_json()
    user_id = current_user.id
    content_type = data.get('content_type')
    content_id = data.get('content_id')
    value = data.get('value')
    errors = {}
    if content_type == "question":
        question = Question.query.get(content_id)
        if not question:
            errors["question"]="Question not found"
    if content_type == "answer":
        answer = Answer.query.get(content_id)
        if not answer:
            errors["answer"]="Answer not found"
    if content_type == "comment":
        comment = Comment.query.get(content_id)
        if not comment:
            errors["comment"]="Comment not found"
    
    if value not in [-1,1]:
        errors["value"]= "value must be -1 or 1."

    if errors:
        return jsonify({"message": "Bad Request","errors": errors}), 400
        
    existing_vote = Vote.query.filter_by( user_id=user_id,
    content_type=content_type, content_id=content_id ).first()

    if existing_vote:
        if existing_vote.value == value:
            existing_vote.value = 0
        else:
            existing_vote.value = value
    else:
        new_vote = Vote(
            user_id=user_id,
            value=value,
            content_type=content_type,
            content_id=content_id
        )
        db.session.add(new_vote)
    db.session.commit()

    if content_type == 'comment':
        content = Comment.query.get(content_id)
        content.update_total_score(db.session)
    elif content_type == 'question':
        content = Question.query.get(content_id)
        content.update_total_score(db.session)
    elif content_type == 'answer':
        content = Answer.query.get(content_id)
        content.update_total_score(db.session)

    return jsonify({"message": "⭐I VOTED!⭐🦅🦅"}), 200
