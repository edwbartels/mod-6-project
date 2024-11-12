from flask import Blueprint, jsonify, request
from flask_login import current_user
from sqlalchemy import asc, desc  # noqa
from ..models.answer import Answer
from ..models.comment import Comment
from ..models.db import db
from ..utils.errors import ValidationError
from ..utils.decorator import (
    login_check,
    # question_exist_check,
    # answer_exist_check,
    # comment_for_question_exist_check,
    # comment_for_question_ownership_check,
    # comment_for_answer_exist_check,
    # comment_for_answer_ownership_check,
    collect_query_params,
    existence_check,authorization_check,owner_check
)

bp = Blueprint("comment", __name__, url_prefix="/api/questions")


@bp.route("/<int:question_id>/comments", methods=["GET"])
# @question_exist_check
@existence_check(("Question","question_id"))
@collect_query_params(Comment)
def get_all_comments_for_question(question_id, question, page, per_page, sort_column, sort_order):
    comments = (
        Comment.query.filter_by(content_id=question_id, content_type="question")
        .order_by(sort_order(sort_column))
        .paginate(page=page, per_page=per_page)
    )

    comments_list = [comment.to_dict() for comment in comments]
    return jsonify(
        {
            "page": page,
            "size": len(comments.items),
            "total_pages": comments.pages,
            "comments": comments_list,
        }
    ), 200


@bp.route("/<int:question_id>/answers/<int:answer_id>/comments", methods=["GET"])
# @question_exist_check
@existence_check(("Question","question_id"))
@collect_query_params(Comment)
def get_all_comments_for_an_answer(
    question_id,question, answer_id, page, per_page, sort_column, sort_order
):
    comments = (
        Comment.query.filter_by(content_id=answer_id, content_type="answer")
        .order_by(sort_order(sort_column))
        .paginate(page=page, per_page=per_page)
    )
    comments_list = [comment.to_dict() for comment in comments]
    return jsonify(
        {
            "page": page,
            "size": len(comments.items),
            "total_pages": comments.pages,
            "comments": comments_list,
        }
    ), 200


@bp.route("/<int:question_id>/allcomments", methods=["GET"])
# @question_exist_check
@existence_check(("Question","question_id"))
def get_all_comments(question_id,question):
    comments_list = []

    question_comments = Comment.query.filter_by(
        content_id=question_id, content_type="question"
    ).all()
    for comment in question_comments:
        comments_list.append(comment.to_dict())

    answer_comments = []
    answer_ids = [
        answer.id for answer in Answer.query.filter_by(question_id=question_id).all()
    ]
    for id in answer_ids:
        comments = Comment.query.filter_by(content_id=id, content_type="answer").all()
        answer_comments.extend(comments)

    for comment in answer_comments:
        comments_list.append(comment.to_dict())

    return jsonify({"comments": comments_list}), 200


@bp.route("/<int:question_id>/comments", methods=["POST"])
# @csrf_protect
@login_check
# @question_exist_check
@existence_check(("Question", "question_id"))
def create_comment_for_question(question_id,question):
    data = request.get_json()
    content = data.get("content")
    errors = []
    if not content:
        errors.append(("content","Data is required"))
    if errors:
        raise ValidationError(errors=errors)
    new_comment = Comment(
        user_id=current_user.id,
        content=content,
        content_id=question_id,
        content_type="question",
    )
    db.session.add(new_comment)
    db.session.commit()
    return jsonify({"comment": new_comment.to_dict()}), 201


@bp.route("/<int:question_id>/comments/<int:comment_id>", methods=["PUT"])
# @csrf_protect
@login_check
# @comment_for_question_exist_check
@existence_check(("Question","question_id"),("Comment","comment_id"))
# @comment_for_question_ownership_check
@authorization_check(owner_check,"comment")
def edit_comment_for_question(question_id,question,comment_id,comment):
    data = request.get_json()
    content = data.get("content")
    # print(comment.content_id)
    errors = []
    if not content:
        errors.append(("content","Data is required"))
    elif comment.content_id != question.id:
        errors.append(("comment","comment does not belong to this question"))
    if errors:
        raise ValidationError(errors=errors)
    # comment = Comment.query.get(comment_id)
    comment.content = content
    db.session.commit()
    return jsonify({"comment": comment.to_dict()}), 200


@bp.route("/<int:question_id>/comments/<int:comment_id>", methods=["DELETE"])
# @csrf_protect
@login_check
# @comment_for_question_exist_check
# @comment_for_question_ownership_check
@existence_check(("Question","question_id"),("Comment","comment_id"))
@authorization_check(owner_check,"comment")
def delete_comment_for_question(question_id,question,comment_id,comment):
    # comment = Comment.query.get(comment_id)
    errors = []
    if comment.content_id != question.id:
        errors.append(("comment","comment does not belong to this question"))
    if errors:
        raise ValidationError(errors=errors)
    db.session.delete(comment)
    db.session.commit()
    return jsonify({"message": "comment for question deleted"}), 200


@bp.route("/<int:question_id>/answers/<int:answer_id>/comments", methods=["POST"])
# @csrf_protect
@login_check
# @question_exist_check
# @answer_exist_check
@existence_check(("Question","question_id"),("Answer","answer_id"))
def create_comment_for_answer(question_id,question,answer_id,answer):
    data = request.get_json()
    content = data.get("content")
    # if not content:
    #     return jsonify({"error": "content is required"}), 400
    errors = []
    if answer.question_id != question.id:
        errors.append(("answer","answer does not belong to this question"))
    if not content:
        errors.append(("comment","Data is required"))
    if errors:
        raise ValidationError(errors=errors)
    new_comment = Comment(
        user_id=current_user.id,
        content=content,
        content_id=answer_id,
        content_type="answer",
    )
    db.session.add(new_comment)
    db.session.commit()
    return jsonify({"comment": new_comment.to_dict()}), 201


@bp.route(
    "/<int:question_id>/answers/<int:answer_id>/comments/<int:comment_id>",
    methods=["PUT"],
)
# @csrf_protect
@login_check
# @comment_for_answer_exist_check
# @comment_for_answer_ownership_check
@existence_check(("Question","question_id"),("Answer","answer_id"),("Comment","comment_id"))
@authorization_check(owner_check,"comment")
def edit_comment_for_answer(question_id, question, answer_id, answer, comment_id, comment):
    data = request.get_json()
    content = data.get("content")
    errors = []
    if answer.question_id != question.id:
        errors.append(("answer","answer does not belong to this question"))
    if comment.content_id != answer.id:
        errors.append(("comment","comment does not belong to this answer"))
    if not content:
        errors.append(("comment","Data is required"))
    if errors:
        raise ValidationError(errors=errors)
    comment.content = content
    db.session.commit()
    return jsonify({"comment": comment.to_dict()}), 200


@bp.route(
    "/<int:question_id>/answers/<int:answer_id>/comments/<int:comment_id>",
    methods=["DELETE"],
)
# @csrf_protect
@login_check
# @comment_for_answer_exist_check
# @comment_for_answer_ownership_check
@existence_check(("Question","question_id"),("Answer","answer_id"),("Comment","comment_id"))
@authorization_check(owner_check,"comment")
def delete_comment_for_answer(question_id, question, answer_id, answer, comment_id, comment):
    # comment = Comment.query.get(comment_id)
    errors = []
    if answer.question_id != question.id:
        errors.append(("answer","answer does not belong to this question"))
    if comment.content_id != answer.id:
        errors.append(("comment","comment does not belong to this answer"))
    if errors:
        raise ValidationError(errors=errors)
    db.session.delete(comment)
    db.session.commit()
    return jsonify({"message": "comment for answer deleted"}), 200
