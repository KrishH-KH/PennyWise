
from . import db


class Expense(db.Model):

    __tablename__ = "expenses"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(120),
        nullable=False
    )

    amount = db.Column(
        db.Numeric(12, 2),
        nullable=False
    )

    expense_date = db.Column(
        db.Date,
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    payment_method = db.Column(
        db.String(50),
        nullable=False,
        default="Cash"
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    category_id = db.Column(
        db.Integer,
        db.ForeignKey("categories.id"),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    updated_at = db.Column(
        db.DateTime,
        onupdate=db.func.now()
    )
