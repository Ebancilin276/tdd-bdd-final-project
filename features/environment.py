"""
Behave Environment Setup

This module configures the behave environment for BDD testing,
including starting and stopping the Flask test server.
"""
import os
import threading
import time
from wsgiref.simple_server import make_server
from service import app, db


BASE_URL = os.getenv("BASE_URL", "http://localhost:8080")

def before_all(context):
    """Setup the test environment before all tests"""
    context.base_url = BASE_URL
    context.data = {}
    context.search_results = []
    context.message = ""
    context.clipboard = ""

    # Start the Flask app in a background thread
    context.server = make_server("0.0.0.0", 8080, app)
    context.server_thread = threading.Thread(target=context.server.serve_forever)
    context.server_thread.daemon = True

    with app.app_context():
        db.create_all()

    context.server_thread.start()
    time.sleep(1)  # Give the server time to start


def before_scenario(context, scenario):
    """Reset data before each scenario"""
    context.data = {}
    context.search_results = []
    context.message = ""
    context.clipboard = ""


def after_all(context):
    """Cleanup after all tests"""
    context.server.shutdown()
