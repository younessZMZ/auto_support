from .base_task import BaseTask
from flask import current_app


class FirstTask(BaseTask):
    def __init__(self, params):
        super().__init__(params)
        self.description = "First Task"
        self.inputs = [
            {"type": "text", "name": "param1", "placeholder": "Enter Param1"},
            {"type": "text", "name": "param2", "placeholder": "Enter Param2"}
        ]
        self.file_upload = True

    def run(self):
        # Perform some task here
        current_app.logger.info("Executing FirstClas with params: ", self.params)
        result = "Class-based task completed with params: " + str(self.params)
        return result
