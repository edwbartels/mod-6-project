from flask import Blueprint, jsonify, request
from flask_login import current_user
from sqlalchemy import asc, desc  # noqa
from ..models.answer import Answer
from ..models.db import db
from ..utils.errors import ValidationError
from ..utils.decorator import (
    login_check,
    collect_query_params,
    existence_check,
    authorization_check,
    owner_check,
)

bp = Blueprint("answer", __name__, url_prefix="/api/questions")


@bp.route(
    "/<int:question_id>/answers", methods=["GET"], endpoint="get_answers_for_question"
)
@collect_query_params(Answer)
def get_all_answers_by_questionId(question_id, page, per_page, sort_column, sort_order):
    answers = (
        Answer.query.filter_by(question_id=question_id)
        .order_by(sort_order(sort_column))
        .paginate(page=page, per_page=per_page)
    )
    answers_list = [answer.to_dict() for answer in answers.items]
    return jsonify(
        {
            "page": page,
            "size": len(answers.items),
            "total_pages": answers.pages,
            "answers": answers_list,
        }
    ), 200


@bp.route(
    "/all/answers/current", methods=["GET"], endpoint="get_answers_for_current_user"
)
@login_check
@collect_query_params(Answer)
def get_all_answers_by_current_user(page, per_page, sort_column, sort_order):
    answers = (
        Answer.query.filter_by(user_id=current_user.id)
        .order_by(sort_order(sort_column))
        .paginate(page=page, per_page=per_page)
    )
    answers_list = [answer.to_dict() for answer in answers]
    return jsonify(
        {
            "page": page,
            "size": len(answers.items),
            "total_pages": answers.pages,
            "answers": answers_list,
        }
    ), 200


@bp.route("/<int:question_id>/answers/current", methods=["GET"])
@existence_check(("Question", "question_id"))
def get_all_answers_by_questionId_and_currentUser(question_id, question):
    answers = Answer.query.filter_by(
        question_id=question_id, user_id=current_user.id
    ).all()
    answers_list = [answer.to_dict() for answer in answers]
    return jsonify({"answers": answers_list}), 200


@bp.route("/<int:question_id>/answers", methods=["POST"])
@login_check
@existence_check(("Question", "question_id"))
def create_answer_by_questionId(question_id, question):
    data = request.get_json()
    new_content = data.get("content")
    if not new_content:
        return jsonify({"error": "Content is required"}), 400
    new_answer = Answer(
        user_id=current_user.id,
        question_id=question_id,
        content=data["content"],
    )
    db.session.add(new_answer)
    db.session.commit()
    return jsonify({"answer": new_answer.to_dict()}), 201


@bp.route("/<int:question_id>/answers/<int:answer_id>", methods=["PUT"])
@login_check
@existence_check(("Question", "question_id"), ("Answer", "answer_id"))
@authorization_check(owner_check, "answer")
def edit_answer_by_questionId_and_answerId(question_id, question, answer_id, answer):
    data = request.get_json()
    new_content = data.get("content")
    if not new_content:
        return jsonify({"error": "Content is required"}), 400
    answer.content = new_content
    db.session.commit()
    return jsonify({"answer": answer.to_dict()}), 200


@bp.route("/<int:question_id>/answers/<int:answer_id>", methods=["DELETE"])
@login_check
@existence_check(("Question", "question_id"), ("Answer", "answer_id"))
@authorization_check(owner_check, "answer")
def delete_answer_by_questionId_and_answerId(question_id, question, answer_id, answer):
    if answer.question_id != question_id:
        raise ValidationError(
            errors=[("Answer", "answer does not belong to this question")]
        )
    db.session.delete(answer)
    db.session.commit()
    return jsonify({"message": "answer deleted"})


@bp.route("/<int:question_id>/answers/<int:answer_id>/accept", methods=["PUT"])
@login_check
@existence_check(("Question", "question_id"), ("Answer", "answer_id"))
@authorization_check(owner_check, "answer")
def mark_answer_accepted_by_questionId_and_answerId(
    question_id, question, answer_id, answer
):
    if answer.question_id != question_id:
        raise ValidationError(
            errors=[("Answer", "answer does not belong to this question")]
        )
    answer.accepted = not answer.accepted
    db.session.commit()
    return jsonify({"answer": answer.to_dict()}), 200
