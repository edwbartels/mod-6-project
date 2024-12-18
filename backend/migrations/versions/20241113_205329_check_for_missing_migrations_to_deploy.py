"""check for missing migrations to deploy

Revision ID: 178b815c5784
Revises:
Create Date: 2024-11-13 20:53:29.001425

"""

from alembic import op
import sqlalchemy as sa
import os


# revision identifiers, used by Alembic.
revision = "178b815c5784"
down_revision = None
branch_labels = None
depends_on = None

schema = "ask_geeves" if os.getenv("FLASK_ENV") == "production" else None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "tags",
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        schema=schema,
    )
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=24), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("_hashed_password", sa.String(length=255), nullable=False),
        sa.Column("first_name", sa.String(length=100), nullable=False),
        sa.Column("last_name", sa.String(length=100), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("username"),
        schema=schema,
    )
    op.create_table(
        "comments",
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("content_id", sa.Integer(), nullable=False),
        sa.Column("content_type", sa.String(length=20), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("total_score", sa.Integer(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["ask_geeves.users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        schema=schema,
    )
    op.create_table(
        "follow_data",
        sa.Column("followed_by_id", sa.Integer(), nullable=False),
        sa.Column("following_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["followed_by_id"],
            ["ask_geeves.users.id"],
        ),
        sa.ForeignKeyConstraint(
            ["following_id"],
            ["ask_geeves.users.id"],
        ),
        sa.PrimaryKeyConstraint("followed_by_id", "following_id"),
        schema=schema,
    )
    op.create_table(
        "questions",
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("total_score", sa.Integer(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["ask_geeves.users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        schema=schema,
    )
    op.create_table(
        "saves",
        sa.Column("content_id", sa.Integer(), nullable=False),
        sa.Column("content_type", sa.String(length=20), nullable=False),
        sa.Column("parent_type", sa.String(length=20), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["ask_geeves.users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "user_id", "content_type", "content_id", name="unique_save_user"
        ),
        schema=schema,
    )
    op.create_table(
        "votes",
        sa.Column("value", sa.Integer(), nullable=False),
        sa.Column("content_type", sa.String(), nullable=False),
        sa.Column("content_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.CheckConstraint("value IN (-1, 0, 1)", name="check_vote_value"),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["ask_geeves.users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "content_type", "content_id"),
        schema=schema,
    )
    op.create_table(
        "answers",
        sa.Column("question_id", sa.Integer(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("accepted", sa.Boolean(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("total_score", sa.Integer(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["question_id"],
            ["ask_geeves.questions.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["ask_geeves.users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        schema=schema,
    )
    op.create_table(
        "question_tags",
        sa.Column("question_id", sa.Integer(), nullable=False),
        sa.Column("tag_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["question_id"],
            ["ask_geeves.questions.id"],
        ),
        sa.ForeignKeyConstraint(
            ["tag_id"],
            ["ask_geeves.tags.id"],
        ),
        sa.PrimaryKeyConstraint("question_id", "tag_id"),
        schema=schema,
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("question_tags", schema=schema)
    op.drop_table("answers", schema=schema)
    op.drop_table("votes", schema=schema)
    op.drop_table("saves", schema=schema)
    op.drop_table("questions", schema=schema)
    op.drop_table("follow_data", schema=schema)
    op.drop_table("comments", schema=schema)
    op.drop_table("users", schema=schema)
    op.drop_table("tags", schema=schema)
    # ### end Alembic commands ###
