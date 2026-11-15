
from datetime import date
from decimal import Decimal

from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    abort
)

from flask_login import login_required, current_user
from sqlalchemy import or_

from models import db, Expense, Category
from forms.expense_forms import ExpenseForm


expenses = Blueprint(
    "expenses",
    __name__,
    url_prefix="/expenses"
)


def get_user_categories():
    return Category.query.filter(
        or_(
            Category.user_id.is_(None),
            Category.user_id == current_user.id
        )
    ).order_by(Category.name.asc()).all()


def configure_form(form):

    categories = get_user_categories()

    form.category_id.choices = [
        (category.id, category.name)
        for category in categories
    ]

    return categories


def get_expense_or_404(expense_id):

    expense = Expense.query.filter_by(
        id=expense_id,
        user_id=current_user.id
    ).first()

    if expense is None:
        abort(404)

    return expense


def category_belongs_to_user(category_id):

    return Category.query.filter(
        Category.id == category_id,
        or_(
            Category.user_id.is_(None),
            Category.user_id == current_user.id
        )
    ).first() is not None


@expenses.route("/")
@login_required
def index():

    query = Expense.query.filter_by(
        user_id=current_user.id
    )

    search = request.args.get("search", "").strip()
    category_id = request.args.get("category", type=int)
    start_date = request.args.get("start_date", "").strip()
    end_date = request.args.get("end_date", "").strip()

    if search:
        query = query.filter(
            Expense.title.ilike(f"%{search}%")
        )

    if category_id:
        query = query.filter(
            Expense.category_id == category_id
        )

    if start_date:
        try:
            query = query.filter(
                Expense.expense_date >= date.fromisoformat(start_date)
            )
        except ValueError:
            flash("Invalid start date.", "warning")

    if end_date:
        try:
            query = query.filter(
                Expense.expense_date <= date.fromisoformat(end_date)
            )
        except ValueError:
            flash("Invalid end date.", "warning")

    pagination = query.order_by(
        Expense.expense_date.desc(),
        Expense.id.desc()
    ).paginate(
        page=request.args.get("page", 1, type=int),
        per_page=10,
        error_out=False
    )

    categories = get_user_categories()

    return render_template(
        "expenses/index.html",
        expenses=pagination.items,
        pagination=pagination,
        categories=categories,
        search=search,
        selected_category=category_id,
        start_date=start_date,
        end_date=end_date
    )


@expenses.route("/add", methods=["GET", "POST"])
@login_required
def add():

    form = ExpenseForm()
    categories = configure_form(form)

    if not categories:
        flash("Please create an expense category first.", "warning")
        return redirect(url_for("expenses.index"))

    if form.validate_on_submit():

        if not category_belongs_to_user(form.category_id.data):
            abort(403)

        expense = Expense(
            title=form.title.data.strip(),
            amount=form.amount.data,
            expense_date=form.expense_date.data,
            description=form.description.data,
            payment_method=form.payment_method.data,
            category_id=form.category_id.data,
            user_id=current_user.id
        )

        try:
            db.session.add(expense)
            db.session.commit()

            flash("Expense added successfully!", "success")

            return redirect(url_for("expenses.index"))

        except Exception:
            db.session.rollback()
            flash("Unable to save expense. Please try again.", "danger")

    return render_template(
        "expenses/form.html",
        form=form,
        page_title="Add New Expense"
    )


@expenses.route("/edit/<int:expense_id>", methods=["GET", "POST"])
@login_required
def edit(expense_id):

    expense = get_expense_or_404(expense_id)

    form = ExpenseForm(obj=expense)
    categories = configure_form(form)

    if form.validate_on_submit():

        if not category_belongs_to_user(form.category_id.data):
            abort(403)

        expense.title = form.title.data.strip()
        expense.amount = form.amount.data
        expense.expense_date = form.expense_date.data
        expense.description = form.description.data
        expense.payment_method = form.payment_method.data
        expense.category_id = form.category_id.data

        try:
            db.session.commit()

            flash("Expense updated successfully!", "success")

            return redirect(url_for("expenses.index"))

        except Exception:
            db.session.rollback()
            flash("Unable to update expense.", "danger")

    return render_template(
        "expenses/form.html",
        form=form,
        page_title="Edit Expense"
    )


@expenses.route("/delete/<int:expense_id>", methods=["POST"])
@login_required
def delete(expense_id):

    expense = get_expense_or_404(expense_id)

    try:
        db.session.delete(expense)
        db.session.commit()

        flash("Expense deleted successfully.", "success")

    except Exception:
        db.session.rollback()
        flash("Unable to delete expense.", "danger")

    return redirect(url_for("expenses.index"))
