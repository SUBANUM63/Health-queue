"""
main

This module defines the main Blueprint for the application, handling home and about pages.

Functions:
    home(): Renders the home page, paginating queues.
    about(): Renders the about page.
"""

from flask import render_template, request, Blueprint
from healthqueue.models import Queue

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    """Renders the home page, paginating queues.

        Args:
            page (int, optional): The page number for pagination. Defaults to 1.

        Returns:
            str: The rendered home page template with paginated queues.
    """
    page = request.args.get('page', 1, type=int)
    queues = Queue.query.order_by(Queue.date_queued.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', queues=queues)


@main.route("/about")
def about():
    """Renders the about page.

       Returns:
           str: The rendered about page template.
    """
    return render_template('about.html', title='About')
