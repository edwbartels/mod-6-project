from .db import db
from .base_models import BelongsToUser


class Vote(BelongsToUser):
    value = db.Column(db.Integer, nullable=False)
    content_type = db.Column(db.String, nullable=False)
    content_id = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        db.UniqueConstraint("user_id", "content_type", "content_id"),
        db.CheckConstraint("value IN (-1, 0, 1)", name="check_vote_value"),
    )

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "content_type": self.content_type,
            "content_id": self.content_id,
            "value": self.value,
        }

    def to_dict_session(self):
        return {
            "content_type": self.content_type,
            "content_id": self.content_id,
            "value": self.value,
        }
