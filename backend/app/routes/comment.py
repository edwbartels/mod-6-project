from flask import Blueprint,jsonify,request
from flask_login import current_user
from ..models.answer import Answer
from ..models.comment import Comment
from ..models.db import db
from ..utils.decorator import (login_check,question_exist_check,
answer_exist_check,comment_for_question_exist_check,
comment_for_question_ownership_check,comment_for_answer_exist_check,comment_for_answer_ownership_check)

bp = Blueprint("comment", __name__, url_prefix="/api/questions")

@bp.route("/<int:question_id>/comments", methods=["GET"])
@question_exist_check
def get_all_comments_for_question(question_id):
    comments = Comment.query.filter_by(content_id=question_id, content_type='question').all()
    comments_list = [comment.to_dict() for comment in comments]
    return jsonify({"comments": comments_list}), 200

@bp.route("/<int:question_id>/answers/<int:answer_id>/comments", methods=["GET"])
@question_exist_check
def get_all_comments_for_an_answer(question_id, answer_id):
    comments = Comment.query.filter_by(content_id=answer_id, content_type='answer').all()
    comments_list = [comment.to_dict() for comment in comments]
    return jsonify({"comments": comments_list}), 200

@bp.route("/<int:question_id>/allcomments", methods=["GET"])
@question_exist_check
def get_all_comments(question_id):
    comments_list = []

    question_comments = Comment.query.filter_by(content_id=question_id, content_type='question').all()
    for comment in question_comments:
        comments_list.append(comment.to_dict())

    answer_comments = []
    answer_ids = [answer.id for answer in Answer.query.filter_by(question_id=question_id).all()]
    for id in answer_ids:
        comments = Comment.query.filter_by(content_id=id, content_type='answer').all()
        answer_comments.extend(comments)

    for comment in answer_comments:
        comments_list.append(comment.to_dict())

    return jsonify({"comments": comments_list}), 200

@bp.route("/<int:question_id>/comments", methods=["POST"])
@login_check
@question_exist_check
def create_comment_for_question(question_id):
    data = request.get_json()
    content = data.get("content")
    if not content:
        return jsonify({"error":"content is required"}),400
    new_comment = Comment(
        user_id=current_user.id,
        content=content,
        content_id=question_id,
        content_type="question"
    )
    db.session.add(new_comment)
    db.session.commit()
    return jsonify({"comment": new_comment.to_dict()}), 201

@bp.route("/<int:question_id>/comments/<int:comment_id>", methods=["PUT"])
@login_check
@comment_for_question_exist_check
@comment_for_question_ownership_check
def edit_comment_for_question(question_id,comment_id):
    data = request.get_json()
    new_content = data.get("content")
    if not new_content:
        return jsonify({"error":"content is required"}),400
    comment = Comment.query.get(comment_id)
    comment.content = new_content
    db.session.commit()
    return jsonify({"comment": comment.to_dict()}), 200

@bp.route("/<int:question_id>/comments/<int:comment_id>", methods=["DELETE"])
@login_check
@comment_for_question_exist_check   
@comment_for_question_ownership_check
def delete_comment_for_question(question_id,comment_id):
    comment = Comment.query.get(comment_id)
    db.session.delete(comment)
    db.session.commit()
    return jsonify({"message": "comment for question deleted"}), 200

@bp.route("/<int:question_id>/answers/<int:answer_id>/comments", methods=["POST"])
@login_check
@question_exist_check
@answer_exist_check
def create_comment_for_answer(question_id,answer_id):
    data = request.get_json()
    content = data.get("content")
    if not content:
        return jsonify({"error":"content is required"}),400
    new_comment = Comment(
        user_id=current_user.id,
        content=content,
        content_id=answer_id,
        content_type="answer"
    )
    db.session.add(new_comment)
    db.session.commit()
    return jsonify({"comment": new_comment.to_dict()}), 201

@bp.route("/<int:question_id>/answers/<int:answer_id>/comments/<int:comment_id>", methods=["PUT"])
@login_check
@comment_for_answer_exist_check
@comment_for_answer_ownership_check
def edit_comment_for_answer(question_id,answer_id,comment_id):
    data = request.get_json()
    new_content = data.get("content")
    if not new_content:
        return jsonify({"error":"content is required"}),400
    comment = Comment.query.get(comment_id)
    comment.content = new_content
    db.session.commit()
    return jsonify({"comment": comment.to_dict()}), 200

@bp.route("/<int:question_id>/answers/<int:answer_id>/comments/<int:comment_id>", methods=["DELETE"])
@login_check
@comment_for_answer_exist_check
@comment_for_answer_ownership_check
def delete_comment_for_answer(question_id,answer_id,comment_id):
    comment = Comment.query.get(comment_id)
    db.session.delete(comment)
    db.session.commit()
    return jsonify({"message": "comment for answer deleted"}), 200