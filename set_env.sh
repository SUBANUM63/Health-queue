#!/bin/bash

# Export environment variables directly
export SECRET_KEY='your-secret-key'
export SQLALCHEMY_DATABASE_URI='sqlite:///site.db'
export MAIL_SERVER='smtp.googlemail.com'
export MAIL_PORT=587
export MAIL_USE_TLS=True
export MAIL_USERNAME='zeinuka@gmail.com'
export MAIL_PASSWORD='your-pass-word'

# Print to verify (optional)
echo "SECRET_KEY: $SECRET_KEY"
echo "SQLALCHEMY_DATABASE_URI: $SQLALCHEMY_DATABASE_URI"
echo "MAIL_SERVER: $MAIL_SERVER"
echo "MAIL_PORT: $MAIL_PORT"
echo "MAIL_USE_TLS: $MAIL_USE_TLS"
echo "MAIL_USERNAME: $MAIL_USERNAME"
echo "MAIL_PASSWORD: $MAIL_PASSWORD"
