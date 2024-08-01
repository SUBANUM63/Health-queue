#!/usr/bin/python
"""
This Module script creates a Flask application using the create_app function
from the healthqueue __init__ module.
If run directly, it starts the Flask development server in debug mode.
"""

from healthqueue import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
