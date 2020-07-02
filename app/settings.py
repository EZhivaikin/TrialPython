# Settings common to all environments (development|staging|production)
# Place environment specific settings in env_settings.py
# An example file (env_settings_example.py) can be used as a starting point

import os

# Application settings
APP_NAME = "Spark Equation trial"
APP_SYSTEM_ERROR_SUBJECT_LINE = APP_NAME + " system error"

# Flask settings
CSRF_ENABLED = False

TIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

JSONIFY_PRETTYPRINT_REGULAR = False

MIN_CATEGORIES_COUNT = 1
MAX_CATEGORIES_COUNT = 5

# Flask-SQLAlchemy settings
SQLALCHEMY_TRACK_MODIFICATIONS = False
