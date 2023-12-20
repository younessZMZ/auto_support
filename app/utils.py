from functools import wraps
from time import time

from flask import current_app, jsonify, request, render_template
from inspect import isclass, getmembers
from .tasks.base_task import BaseTask


def find_task_class(module):
    for name, obj in getmembers(module):
        if isclass(obj) and issubclass(obj, BaseTask) and obj is not BaseTask:
            return obj


def is_valid(*args, **kwargs):
    return True


def error_handler(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception as e:
            current_app.logger.error(f"Error in {function.__name__}: {e}")

            # Check if the request accepts JSON response
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                response = jsonify({'error': 'An internal server error occurred', 'details': str(e)})
                response.status_code = 500
                return response
            else:
                # Render an error page for HTML requests
                return render_template('error.html', error_message=str(e)), 500
    return decorated_function


def validate_inputs(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Perform validation logic
        if not is_valid(args, kwargs):
            raise ValueError("Invalid inputs")
        return f(*args, **kwargs)
    return decorated_function


def measure_time(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start_time = time()
        result = f(*args, **kwargs)
        elapsed_time = time() - start_time
        current_app.logger.info(f"{f.__name__} took {elapsed_time:.2f} seconds")
        return result
    return decorated_function
