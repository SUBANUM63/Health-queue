#!/usr/bin/python
"""
This module initializes the HealthQueue application and creates the database tables.

Imports:
    - create_app: Factory function to create and configure the Flask application.
    - db: Database instance from the HealthQueue application.
"""

from healthqueue import create_app, db

# Create the Flask application using the factory function
app = create_app()

with app.app_context():
    """
    Creates all the database tables within the application context.
    Ensures that the database is properly initialized before the application starts.

    Output:
        Prints a success message upon successful creation of the database tables.
    """
    db.create_all()
    print("Database tables created successfully.")
