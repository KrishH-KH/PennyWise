
from datetime import date
from calendar import monthrange

from flask import Blueprint, render_template
from flask_login import login_required, current_user
from sqlalchemy import func

from models import db, Expense, Category

dashboard = Blueprint("dashboard", __name__)


@dashboard.route("/dashboard")
@login_required
def home():
    today = date.today()

    # First and last day of the current month
    month_start = today.replace(day=1)
    month_end = today.replace(
        day=monthrange(today.year, today.month)[1]
    )

    # Previous month boundaries
    if today.month == 1:
        previous_month_start = date(today.year - 1, 12, 1)
    else:
        previous_month_start = date(today.year, today.month - 1, 1)

    previous_month_end = date(
        today.year if today.month > 1 else today.year - 1,
        today.month - 1 if today.month > 1 else 12,
        monthrange(
            previous_month_start.year,
            previous_month_start.month
        )[1]
    )

    # Total spending across all time
    total_expenses = (
        db.session.query(func.coalesce(func.sum(Expense.amount), 0))
        .filter(Expense.user_id == current_user.id)
        .scalar()
    )

    # Spending this month
    monthly_expenses = (
        db.session.query(func.coalesce(func.sum(Expense.amount), 0))
        .filter(
            Expense.user_id == current_user.id,
            Expense.expense_date >= month_start,
            Expense.expense_date <= month_end
        )
        .scalar()
    )

    # Spending today
    today_expenses = (
        db.session.query(func.coalesce(func.sum(Expense.amount), 0))
        .filter(
            Expense.user_id == current_user.id,
            Expense.expense_date == today
        )
        .scalar()
    )

    # Spending last month
    previous_month_expenses = (
        db.session.query(func.coalesce(func.sum(Expense.amount), 0))
        .filter(
            Expense.user_id == current_user.id,
            Expense.expense_date >= previous_month_start,
            Expense.expense_date <= previous_month_end
        )
        .scalar()
    )

    # Monthly percentage change
    if previous_month_expenses:
        monthly_change = (
            (float(monthly_expenses) - float(previous_month_expenses))
            / float(previous_month_expenses)
        ) * 100
    else:
        monthly_change = None

    # Spending grouped by category for this month
    category_data = (
        db.session.query(
            Category.name,
            func.sum(Expense.amount).label("total")
        )
        .join(Expense, Expense.category_id == Category.id)
        .filter(
            Expense.user_id == current_user.id,
            Expense.expense_date >= month_start,
            Expense.expense_date <= month_end
        )
        .group_by(Category.name)
        .order_by(func.sum(Expense.amount).desc())
        .all()
    )

    category_labels = [row.name for row in category_data]
    category_amounts = [float(row.total) for row in category_data]

    # Daily spending for the current month
    daily_data = (
        db.session.query(
            Expense.expense_date,
            func.sum(Expense.amount).label("total")
        )
        .filter(
            Expense.user_id == current_user.id,
            Expense.expense_date >= month_start,
            Expense.expense_date <= today
        )
        .group_by(Expense.expense_date)
        .order_by(Expense.expense_date)
        .all()
    )

    daily_labels = [
        row.expense_date.strftime("%d %b") for row in daily_data
    ]
    daily_amounts = [float(row.total) for row in daily_data]

    # Latest 5 transactions
    recent_expenses = (
        Expense.query
        .filter_by(user_id=current_user.id)
        .order_by(
            Expense.expense_date.desc(),
            Expense.id.desc()
        )
        .limit(5)
        .all()
    )

    return render_template(
        "dashboard/home.html",
        total_expenses=float(total_expenses),
        monthly_expenses=float(monthly_expenses),
        today_expenses=float(today_expenses),
        previous_month_expenses=float(previous_month_expenses),
        monthly_change=monthly_change,
        category_labels=category_labels,
        category_amounts=category_amounts,
        daily_labels=daily_labels,
        daily_amounts=daily_amounts,
        recent_expenses=recent_expenses,
        today=today
    )
