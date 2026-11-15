
from app import app
from models import db, Category

DEFAULT_CATEGORIES = [
    ("Food & Dining", "utensils", "#F59E0B"),
    ("Transportation", "car", "#3B82F6"),
    ("Shopping", "shopping-bag", "#EC4899"),
    ("Education", "graduation-cap", "#8B5CF6"),
    ("Entertainment", "film", "#F97316"),
    ("Healthcare", "heart-pulse", "#EF4444"),
    ("Bills & Utilities", "receipt", "#14B8A6"),
    ("Travel", "plane", "#6366F1"),
    ("Others", "wallet", "#64748B")
]

with app.app_context():

    for name, icon, color in DEFAULT_CATEGORIES:

        existing = Category.query.filter_by(
            name=name,
            user_id=None
        ).first()

        if not existing:

            category = Category(
                name=name,
                icon=icon,
                color=color,
                user_id=None
            )

            db.session.add(category)

    db.session.commit()

    print("Default categories created successfully!")
