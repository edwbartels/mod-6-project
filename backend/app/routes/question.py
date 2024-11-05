from flask import Blueprint, jsonify, request
from flask_login import current_user
from ..models.question import Question
from ..models.tag import Tag
from ..models.db import db
from ..utils.decorator import (
    login_check,
    question_exist_check,
    question_ownership_check,
)

bp = Blueprint("question", __name__, url_prefix="/api/questions")


@bp.route("/", methods=["GET"])
def get_all_questions():
    all_questions = Question.query.all()
    if not all_questions:
        return jsonify({"message": "No questions found"}), 404
    questions_list = []
    for question in all_questions:
        eachQuestion = question.to_dict()
        questions_list.append(eachQuestion)
    return jsonify({"questions": questions_list}), 200


@bp.route("/<int:question_id>", methods=["GET"])
def get_question_by_id(question_id):
    question = Question.query.get(question_id)
    user = question.user
    if question:
        return jsonify(
            {"question": question.to_dict(), "user": question.user.to_dict()}
        )
    else:
        return jsonify({"error": "Question not found"}), 404


@bp.route("/current", methods=["GET"])
@login_check
def get_questions_by_current_user():
    user_questions = Question.query.filter_by(user_id=current_user.id).all()
    questions_list = [question.to_dict() for question in user_questions]
    return jsonify({"questions_owned": questions_list}), 200


@bp.route("/", methods=["POST"])
@login_check
def create_question():
<<<<<<< HEAD
    data = request.get_json()       
    content = data.get("content")
    if not content:
        return jsonify({"error":"content is required"})
    input_tags = data.get("tag") 
    tags = []
    if input_tags:
        for tag_name in input_tags:
            tag_name = tag_name.strip()
            if not tag_name:
                continue
            existing_tag = Tag.query.filter_by(name=tag_name).first()
            if existing_tag:
                tags.append(existing_tag)
            else:
                new_tag = Tag(name=tag_name)
                db.session.add(new_tag)
                tags.append(new_tag)

    new_question = Question(
        user_id=current_user.id,
        content=content,
        tags = tags
=======
    data = request.get_json()
    # ? validate check
    # if not data:
    #     return jsonify({"error": "Content is required"})
    new_question = Question(
        user_id=current_user.id,
        content=data["content"],
        ##?more stuff?
>>>>>>> migrations
    )
    db.session.add(new_question)
    db.session.commit()
    return jsonify({"question": new_question.to_dict()}), 201


@bp.route("/<int:question_id>", methods=["PUT"])
@login_check
@question_exist_check
@question_ownership_check
def edit_question(question_id):
    question = Question.query.get(question_id)
    data = request.get_json()
<<<<<<< HEAD
    new_content = data.get("content")
    if not new_content:
        return jsonify({"error":"content is required"}),400
    question.content = new_content
    db.session.commit()
    return jsonify({"question":question.to_dict()}), 200
=======
    # ? validate check
    # if not data:
    #     return jsonify({"error": "Content is required"})
    question.content = data["content"]
    db.session.commit()

    return jsonify({"question": question.to_dict()}), 200

>>>>>>> migrations

@bp.route("/<int:question_id>", methods=["DELETE"])
@login_check
@question_exist_check
@question_ownership_check
def delete_question(question_id):
    question = Question.query.get(question_id)
    db.session.delete(question)
    db.session.commit()
    return jsonify({"message": "question deleted"}), 200
