
from . import db


class Budget(db.Model):

    __tablename__ = "budgets"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    amount = db.Column(
        db.Numeric(12, 2),
        nullable=False
    )

    month = db.Column(
        db.Integer,
        nullable=False
    )

    year = db.Column(
        db.Integer,
        nullable=False
    )

    category_id = db.Column(
        db.Integer,
        db.ForeignKey("categories.id"),
        nullable=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    category = db.relationship(
        "Category",
        backref="budgets"
    )
