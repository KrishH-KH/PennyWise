
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    DecimalField,
    SelectField,
    DateField,
    TextAreaField,
    SubmitField
)

from wtforms.validators import (
    DataRequired,
    Length,
    NumberRange,
    Optional
)


class ExpenseForm(FlaskForm):

    title = StringField(
        "Expense Title",
        validators=[
            DataRequired(),
            Length(max=120)
        ]
    )

    amount = DecimalField(
        "Amount (INR)",
        places=2,
        validators=[
            DataRequired(),
            NumberRange(min=0.01, max=9999999999.99)
        ]
    )

    expense_date = DateField(
        "Expense Date",
        validators=[DataRequired()]
    )

    category_id = SelectField(
        "Category",
        coerce=int,
        validators=[DataRequired()]
    )

    payment_method = SelectField(
        "Payment Method",
        choices=[
            ("Cash", "Cash"),
            ("UPI", "UPI"),
            ("Credit Card", "Credit Card"),
            ("Debit Card", "Debit Card"),
            ("Net Banking", "Net Banking"),
            ("Other", "Other")
        ],
        validators=[DataRequired()]
    )

    description = TextAreaField(
        "Description",
        validators=[
            Optional(),
            Length(max=1000)
        ]
    )

    submit = SubmitField("Save Expense")
