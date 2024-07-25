from flask import render_template, request, Blueprint
from healthqueue.models import Queue

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    queues = Queue.query.order_by(Queue.date_queued.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', queues=queues)


@main.route("/about")
def about():
    return render_template('about.html', title='About')
