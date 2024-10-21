# task-focus
Task-Focus: A Simple To-Do App with Flask

Task-Focus is a simple web application for task management built using Flask. It supports user registration and login, task CRUD (create, read, update, delete) operations, and provides minimal analytics for users.
Features

    User Registration and Authentication using Flask-Login.
    Task CRUD Operations: Users can create, edit, and delete their own tasks.
    Minimal Analytics: Displays the number of tasks per user.
    User Interface: Built with Bootstrap for a clean and simple UI.

Tech Stack

    Flask — a lightweight Python web framework.
    SQLite — a simple embedded database to store user and task data.
    Flask-Login — for managing user sessions and authentication.
    Bootstrap — for a responsive and clean user interface.

Setup and Installation
Prerequisites

    Python 3.x
    pip (Python package installer)

Installation Steps

1) Clone the repository:

        git clone https://github.com/your-username/task-focus.git
        cd task-focus

2) Set up a virtual environment (optional but recommended):

        python -m venv venv
        source venv/bin/activate  # On Windows: venv\Scripts\activate

3) Install required dependencies:

        pip install -r requirements.txt

4) Set up the SQLite database:

        from app import db
        db.create_all()

5) Run the application:

        flask run
The application will be available at http://127.0.0.1:5000/.

Usage

    Register a new account or log in if you already have an account.
    Create new tasks, edit existing ones, or delete tasks when done.
    Use the "Analytics" section to see basic stats, such as the total number of tasks.

Future Improvements

    Add more detailed task analytics (e.g., completion rate, deadlines approaching).
    Implement task categorization (e.g., work, personal, etc.).
    Add support for priority levels and task deadlines.
