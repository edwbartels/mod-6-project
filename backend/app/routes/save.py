from flask import Blueprint,jsonify
from flask_login import current_user
from ..models.save import Save
from ..models.db import db
from ..utils.decorator import (login_check, question_exist_check,
answer_exist_check, comment_for_question_exist_check,comment_for_answer_exist_check)

bp = Blueprint("save", __name__, url_prefix="/api/questions")

@bp.route("/usersaves")
@login_check
def get_all_saves():
    saves = Save.query.filter_by(user_id=current_user.id).all()
    saves_list = [save.to_dict() for save in saves]
    return jsonify({"all_saves": saves_list}), 200

@bp.route("/<int:question_id>/saves", methods=["POST"])
@login_check
@question_exist_check
def add_question_to_saves(question_id):
    save = Save.query.filter_by(user_id=current_user.id, content_id=question_id, content_type="question").first()
    if save:
        return jsonify({"message": "question already saved"}), 200
    new_save = Save(
        user_id=current_user.id,
        content_id=question_id,
        content_type="question"
    )
    db.session.add(new_save)
    db.session.commit()
    return jsonify({"save": new_save.to_dict()}), 201

@bp.route("/<int:question_id>/saves", methods=["DELETE"])
@login_check
@question_exist_check
def delete_question_from_saves(question_id):
    save = Save.query.filter_by(user_id=current_user.id, content_id=question_id, content_type="question").first()
    if not save:
        return jsonify({"error": "save not found"}), 404
    db.session.delete(save)
    db.session.commit()
    return jsonify({"message": "question deleted from saves"}), 200

@bp.route("/<int:question_id>/answers/<int:answer_id>/saves", methods=["POST"])
@login_check
@answer_exist_check
def add_answer_to_saves(question_id, answer_id):
    save = Save.query.filter_by(user_id=current_user.id, content_id=answer_id, content_type="answer").first()
    if save:
        return jsonify({"message": "answer already saved"}), 200
    new_save = Save(
        user_id=current_user.id,
        content_id=answer_id,
        content_type="answer"
    )
    db.session.add(new_save)
    db.session.commit()
    return jsonify({"save": new_save.to_dict()}), 201

@bp.route("/<int:question_id>/answers/<int:answer_id>/saves", methods=["DELETE"])
@login_check
@answer_exist_check
def delete_answer_from_saves(question_id, answer_id):
    save = Save.query.filter_by(user_id=current_user.id, content_id=answer_id, content_type="answer").first()
    if not save:
        return jsonify({"error": "save not found"}), 404
    db.session.delete(save)
    db.session.commit()
    return jsonify({"message": "answer deleted from saves"}), 200

@bp.route("/<int:question_id>/comments/<int:comment_id>/saves", methods=["POST"])
@login_check
@comment_for_question_exist_check
def add_question_comment_to_saves(question_id, comment_id):
    save = Save.query.filter_by(user_id=current_user.id, content_id=comment_id, content_type="comment").first()
    if save:
        return jsonify({"message": "comment in question already saved"}), 200

    new_save = Save(
        user_id=current_user.id,
        content_id=comment_id,
        content_type="comment",
        parent_type="question"
    )
    db.session.add(new_save)
    db.session.commit()
    return jsonify({"save": new_save.to_dict()}), 201

@bp.route("/<int:question_id>/comments/<int:comment_id>/saves", methods=["DELETE"])
@login_check
@comment_for_question_exist_check
def delete_question_comment_from_saves(question_id, comment_id):
    save = Save.query.filter_by(user_id=current_user.id, content_id=comment_id, content_type="comment").first()
    if not save:
        return jsonify({"error": "save not found"}), 404
    db.session.delete(save)
    db.session.commit()
    return jsonify({"message": "comment in question deleted from saves"}), 200

@bp.route("/<int:question_id>/answers/<int:answer_id>/comments/<int:comment_id>/saves", methods=["POST"])
@login_check
@comment_for_answer_exist_check
def add_answer_comment_to_saves(question_id,answer_id, comment_id):
    save = Save.query.filter_by(user_id=current_user.id, content_id=comment_id, content_type="comment").first()
    if save:
        return jsonify({"message": "comment in answer already saved"}), 200

    new_save = Save(
        user_id=current_user.id,
        content_id=comment_id,
        content_type="comment",
        parent_type="answer"
    )
    db.session.add(new_save)
    db.session.commit()
    return jsonify({"save": new_save.to_dict()}), 201

@bp.route("/<int:question_id>/answers/<int:answer_id>/comments/<int:comment_id>/saves", methods=["DELETE"])
@login_check
@comment_for_answer_exist_check
def delete_answer_comment_from_saves(question_id,answer_id, comment_id):
    save = Save.query.filter_by(user_id=current_user.id, content_id=comment_id, content_type="comment").first()
    if not save:
        return jsonify({"error": "save not found"}), 404
    db.session.delete(save)
    db.session.commit()
    return jsonify({"message": "comment in answer deleted from saves"}), 200
