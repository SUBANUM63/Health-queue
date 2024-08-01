#!/usr/bin/python
"""
This Module script is for handling errors on the health queue flask application
"""

from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def error_404(error):
    """
    Handle 404 errors (Page Not Found).

    This function renders the 404 error page template.

    Args:
        error: The error object containing information about the 404 error.

    Returns:
        tuple: Rendered template for 404 error and the status code 404.
    """
    return render_template('errors/404.html'), 404


@errors.app_errorhandler(403)
def error_403(error):
    """
    Handle 403 errors (Forbidden).

    This function renders the 403 error page template.

    Args:
        error: The error object containing information about the 403 error.

    Returns:
        tuple: Rendered template for 403 error and the status code 403.
    """
    return render_template('errors/403.html'), 403


@errors.app_errorhandler(500)
def error_500(error):
    """
    Handle 500 errors (Internal Server Error).

    This function renders the 500 error page template.

    Args:
        error: The error object containing information about the 500 error.

    Returns:
        tuple: Rendered template for 500 error and the status code 500.
    """
    return render_template('errors/500.html'), 500
