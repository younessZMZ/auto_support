from flask import Blueprint, render_template, request, jsonify, current_app
import os
import importlib
from werkzeug.utils import secure_filename
from .tasks.base_task import BaseTask
from .utils import find_task_class, error_handler
from logging import getLogger


logger = getLogger(__name__)

main = Blueprint("main", __name__)

tasks_path = "./app/tasks"
tasks = [
    f.split(".")[0]
    for f in os.listdir(tasks_path)
    if f != "base_task.py" and f.endswith(".py") and not f.startswith("__")
]


@main.route("/")
@error_handler
def index():
    current_app.logger.info("Loading the index page.")
    task_configs = {}
    task_descriptions = {}
    for task_name in tasks:
        task_module = importlib.import_module(f".tasks.{task_name}", package="app")
        task_class = find_task_class(task_module)
        if issubclass(task_class, BaseTask):
            task_instance = task_class({})
            task_configs[task_name] = task_instance.get_input_config()
            task_descriptions[task_name] = task_instance.description
        else:
            task_configs[task_name] = {"inputs": [], "fileUpload": False}

    return render_template("index.html", tasks=tasks, task_configs=task_configs, task_descriptions=task_descriptions)


@main.route("/run_task", methods=["POST"])
@error_handler
def run_task():
    task_name = request.form.get("task")
    uploaded_file = request.files.get("file")
    params = {key: request.form[key] for key in request.form if key != "task"}
    if uploaded_file:
        filename = secure_filename(uploaded_file.filename)
        file_path = os.path.join("uploads", filename)
        uploaded_file.save(file_path)
        params["file_path"] = file_path

    if task_name in tasks:
        task_module = importlib.import_module(f".tasks.{task_name}", package="app")
        task_class = find_task_class(task_module)
        if issubclass(task_class, BaseTask):
            task_instance = task_class(params)
            result = task_instance.run()
            return jsonify(result)
        else:
            return jsonify({'error': 'Invalid task class'}), 400
    else:
        return jsonify({"error": "Task not found"}), 404


@main.route("/index")
def new_index():
    return render_template("home/index.html", segment="index")
