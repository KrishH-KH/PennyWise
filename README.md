# PennyWise — Personal Expense Management

PennyWise is a web-based personal expense management application built with Flask. It helps users record expenses, organize spending by category, and understand their spending habits through an interactive dashboard.

The project focuses on making everyday expense tracking simple through a clean interface and a lightweight database.

## Features

- **User Authentication** — User registration and login with securely hashed passwords.
- **Expense Management** — Add, view, edit and delete expense records.
- **Expense Organization** — Organize transactions using categories.
- **Dashboard** — View an overview of expenses and recent transactions.
- **Spending Visualizations** — Interactive charts for category-wise and daily expense breakdowns.
- **Monthly Overview** — View spending totals and monthly comparisons.
- **INR Support** — Expense amounts are displayed in Indian Rupees.
- **Responsive Interface** — Built with Bootstrap for a clean user experience.

## Tech Stack

| Component | Technology |
|---|---|
| Backend | Python, Flask |
| Frontend | HTML, CSS, JavaScript |
| UI Framework | Bootstrap 5 |
| Charts | Chart.js |
| Database | SQLite |
| ORM | Flask-SQLAlchemy |
| Database Migrations | Flask-Migrate |
| Authentication | Flask-Login |
| Forms & CSRF Protection | Flask-WTF |

## Project Structure

```text
PennyWise/
├── app.py
├── config.py
├── requirements.txt
├── seed_categories.py
├── .env.example
│
├── forms/
├── models/
├── routes/
├── migrations/
│
├── templates/
│   ├── auth/
│   ├── dashboard/
│   └── expenses/
│
└── static/
    ├── css/
    ├── js/
    └── images/
```

## Getting Started

Follow these steps to run PennyWise locally.

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/PennyWise.git
cd PennyWise
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create your local `.env` file from the example:

```bash
copy .env.example .env
```

Open `.env` and replace the placeholder secret key with your own secure random value.

Example:

```env
SECRET_KEY=your-own-secret-key
DATABASE_URL=sqlite:///pennywise.db
```

**Important:** Never upload your actual `.env` file or database credentials to GitHub.

### 5. Initialize the database

Apply the database migrations:

```bash
flask --app app db upgrade
```

### 6. Seed default categories

```bash
python seed_categories.py
```

### 7. Run the application

```bash
python app.py
```

Open the local application in your browser at:

```text
http://127.0.0.1:5000/
```

## Security

- Passwords are stored using password hashing rather than plain text.
- CSRF protection is implemented for forms.
- Environment-specific configuration is kept outside the repository.
- Local database files and virtual environments are excluded from version control.

## Planned Improvements

- Budget creation and tracking.
- Detailed expense reports.
- Data export functionality.
- Additional spending insights and analytics.

## License

License details have not yet been specified.
