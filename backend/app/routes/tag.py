from flask import Blueprint, jsonify, request
from ..models.tag import Tag
from ..models.question import Question
from ..utils.errors import ValidationError
from ..models.db import db
from ..utils.decorator import (
    login_check,
    existence_check,
    authorization_check,
    owner_check,
)

bp = Blueprint("tags", __name__, url_prefix="/api/questions")


@bp.route("/tags")
def get_all_tags():
    tags = Tag.query.all()
    tag_list = []
    for tag in tags:
        tag_list.append(tag.to_dict())
    return jsonify({"tags": tag_list}), 200


@bp.route("/<int:question_id>/tags", methods=["GET"])
@existence_check(("Question", "question_id"))
def get_all_tags_by_questionId(question_id, question):
    tags = question.tags
    tags_list = [tag.to_dict() for tag in tags]
    return jsonify({"tags": tags_list}), 200


@bp.route("/<int:question_id>/tags", methods=["POST"])
@login_check
@existence_check(("Question", "question_id"))
@authorization_check(owner_check, "question")
def add_tag_to_question(question_id, question):
    tags_list = [tag.to_dict() for tag in question.tags]
    data = request.get_json()
    input_tag = data.get("tag")

    exist_tag = Tag.query.filter_by(name=input_tag).first()

    if exist_tag:
        if exist_tag not in question.tags:
            question.tags.append(exist_tag)
            db.session.commit()
            tags_list = [tag.to_dict() for tag in question.tags]
            return jsonify({"tags": tags_list}), 201
        else:
            return jsonify(
                {"message": "Validation Error", "error": "tag already exist"}
            ), 400
    else:
        new_tag = Tag(name=input_tag)
        db.session.add(new_tag)
        question.tags.append(new_tag)
        db.session.commit()
        tags_list = [tag.to_dict() for tag in question.tags]
        return jsonify({"tags": tags_list}), 201


@bp.route("/<int:question_id>/tags/<int:tag_id>", methods=["DELETE"])
@login_check
@existence_check(("Question", "question_id"), ("Tag", "tag_id"))
@authorization_check(owner_check, "question")
def delete_tag_from_question(question_id, question, tag_id, tag):
    if tag not in question.tags:
        raise ValidationError(errors=[("Tag", "tag did not add to this question")])
    question.tags.remove(tag)
    db.session.commit()
    return jsonify({"message": "tag removed"}), 200
