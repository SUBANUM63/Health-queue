#!/usr/bin/python
"""
This module defines the routes for handling queue-related actions in the HealthQueue application.

Imports:
    - render_template: Renders a template with the given context.
    - url_for: Generates URLs to the given endpoint.
    - flash: Displays a message to the user.
    - redirect: Redirects the user to a different endpoint.
    - request: Handles request data in routes.
    - abort: Aborts a request with a given status code.
    - Blueprint: Registers a group of routes.
    - current_user: Gets the currently logged-in user.
    - login_required: Ensures a route is accessed only by logged-in users.
    - db: Database instance from the HealthQueue application.
    - Queue: Queue model from the HealthQueue application.
    - QueueForm: Form for creating and updating queue entries.
"""

from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from healthqueue import db
from healthqueue.models import Queue
from healthqueue.queues.forms import QueueForm

queues = Blueprint('queues', __name__)


@queues.route("/queue/new", methods=['GET', 'POST'])
@login_required
def new_queue():
    """Renders the queue creation form, processes submission, creates a new
    Queue object, and redirects to the home page.

    Returns:
        str: The rendered queue creation template with form.
    """
    form = QueueForm()
    if form.validate_on_submit():
        queue = Queue(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(queue)
        db.session.commit()
        flash('Your queue has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_queue.html', title='New Queue',
                           form=form, legend='New Queue')


@queues.route("/queue/<int:queue_id>")
def queue(queue_id):
    """Retrieves a Queue object by ID, renders its details.

    Args:
        queue_id (int): The ID of the Queue object to retrieve.

    Returns:
        str: The rendered queue details template.
    """
    queue = Queue.query.get_or_404(queue_id)
    return render_template('queue.html', title=queue.title, queue=queue)


@queues.route("/queue/<int:queue_id>/update", methods=['GET', 'POST'])
@login_required
def update_queue(queue_id):
    """Retrieves a Queue object, renders the update form, processes submission,
    updates the object, and redirects to the queue details page.

    Args:
        queue_id (int): The ID of the Queue object to update.

    Returns:
        str: The rendered queue update template with form.
    """
    queue = Queue.query.get_or_404(queue_id)
    if queue.author != current_user:
        abort(403)
    form = QueueForm()
    if form.validate_on_submit():
        queue.title = form.title.data
        queue.content = form.content.data
        db.session.commit()
        flash('Your queue has been updated!', 'success')
        return redirect(url_for('queues.queue', queue_id=queue.id))
    elif request.method == 'GET':
        form.title.data = queue.title
        form.content.data = queue.content
    return render_template('create_queue.html', title='Update Queue',
                           form=form, legend='Update Queue')


@queues.route("/queue/<int:queue_id>/delete", methods=['POST'])
@login_required
def delete_queue(queue_id):
    """Retrieves a Queue object, deletes it, and redirects to the home page.

    Args:
        queue_id (int): The ID of the Queue object to delete.

    Returns:
        str: Redirection to the home page.
    """
    queue = Queue.query.get_or_404(queue_id)
    if queue.author != current_user:
        abort(403)
    db.session.delete(queue)
    db.session.commit()
    flash('Your queue has been deleted!', 'success')
    return redirect(url_for('main.home'))
