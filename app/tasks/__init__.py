"""
In this package each module represents a task, except the base class which is the parent of all task classes.

Here are the rules for adding tasks:
- Add a new module.
- Define the class task inside the module which will inherit from BaseTask.
- Define the attributes: description, inputs, upload_file.
- Define the function run of the task class.
"""