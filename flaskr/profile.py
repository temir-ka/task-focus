from flask import (
    Blueprint, flash, redirect, render_template, url_for, request
)
from .db import db, Task
from .auth import login_required, current_user
from datetime import datetime
from sqlalchemy.sql import func



bp = Blueprint('profile', __name__)


@bp.route('/')
def home():
    if current_user.is_authenticated:
        tasks = Task.query.filter_by(user_id=current_user.id).all()
    else:
        tasks = []
    return render_template('index.html', tasks=tasks)


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        deadline_str = request.form['deadline']
        error = None

        if not title:
            error = 'Title is required'

        if not deadline_str:
            error = 'Deadline is required'
        
        if error is not None:
            flash(error, 'danger')
        else:
            deadline = datetime.strptime(deadline_str, '%Y-%m-%dT%H:%M')
            task = Task(title=title, description=description, deadline=deadline, user_id=current_user.id)
            db.session.add(task)
            db.session.commit()
            flash('Successfully created', 'success')
            return redirect(url_for('profile.home'))
    return render_template("create.html")

@bp.route('/update_task_status', methods=['POST'])
@login_required
def update_task_status():
    task_id = request.form.get('task_id')
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()

    if task:
        # Если чекбокс был отмечен, то поле 'completed' будет присутствовать в запросе
        task.completed = 'completed' in request.form

        db.session.commit()

    return redirect(url_for('profile.home'))

@bp.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        deadline_str = request.form['deadline']
        error = None

        if not title:
            error = 'Title is required'

        if not deadline_str:
            error = 'Deadline is required'
        
        if error is not None:
            flash(error, 'danger')
        else:
            task.title = title
            task.description = description
            task.deadline = datetime.strptime(deadline_str, '%Y-%m-%dT%H:%M')
            db.session.commit()
            flash('Task updated successfully', 'success')
            return redirect(url_for('profile.home'))
    
    return render_template("edit_task.html", task=task)

@bp.route('/delete_task/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task and task.user_id == current_user.id:
        db.session.delete(task)
        db.session.commit()
        flash('Task deleted successfully!', 'success')
    else:
        flash('Task not found or permission denied.', 'danger')
    
    return redirect(url_for('profile.home'))


@bp.route('/analytics', methods=['GET'])
@login_required
def analytics():
    # Количество выполненных задач
    completed_tasks_count = Task.query.filter_by(user_id=current_user.id, completed=True).count()

    # Количество невыполненных задач
    incomplete_tasks_count = Task.query.filter_by(user_id=current_user.id, completed=False).count()

    # Количество просроченных задач (где срок выполнения меньше текущей даты и задача не выполнена)
    overdue_tasks_count = Task.query.filter(Task.deadline < datetime.utcnow(), Task.completed == False, Task.user_id == current_user.id).count()

    # Процент выполненных задач
    total_tasks_count = completed_tasks_count + incomplete_tasks_count
    if total_tasks_count > 0:
        completed_percentage = (completed_tasks_count / total_tasks_count) * 100
    else:
        completed_percentage = 0

    # Среднее время выполнения задачи (от создания до завершения)
    average_completion_time = db.session.query(func.avg(func.julianday(Task.deadline) - func.julianday(Task.created_date)))\
                                        .filter_by(user_id=current_user.id, completed=True)\
                                        .scalar()

    if average_completion_time:
        average_completion_time = round(average_completion_time, 2)
    else:
        average_completion_time = "No completed tasks yet"

    return render_template("analytics.html", 
                           completed_tasks_count=completed_tasks_count, 
                           incomplete_tasks_count=incomplete_tasks_count,
                           overdue_tasks_count=overdue_tasks_count,
                           completed_percentage=completed_percentage,
                           average_completion_time=average_completion_time)