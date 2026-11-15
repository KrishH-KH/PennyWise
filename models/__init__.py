
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

# Import models so SQLAlchemy and Flask-Migrate can detect them
from .user import User
from .category import Category
from .expense import Expense
from .budget import Budget
