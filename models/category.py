
from . import db


class Category(db.Model):

    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(80),
        nullable=False
    )

    icon = db.Column(
        db.String(50),
        default="wallet"
    )

    color = db.Column(
        db.String(20),
        default="#36C99A"
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True
    )

    expenses = db.relationship(
        "Expense",
        backref="category",
        lazy=True
    )
