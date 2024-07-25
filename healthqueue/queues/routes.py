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
    queue = Queue.query.get_or_404(queue_id)
    return render_template('queue.html', title=queue.title, queue=queue)


@queues.route("/queue/<int:queue_id>/update", methods=['GET', 'POST'])
@login_required
def update_queue(queue_id):
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
    queue = Queue.query.get_or_404(queue_id)
    if queue.author != current_user:
        abort(403)
    db.session.delete(queue)
    db.session.commit()
    flash('Your queue has been deleted!', 'success')
    return redirect(url_for('main.home'))
