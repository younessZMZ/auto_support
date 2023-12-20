from .base_task import BaseTask


class SecondTask(BaseTask):
    def __init__(self, params):
        super().__init__(params)
        self.description = "Second Task"
        self.file_upload = True

    def run(self):
        # Perform some task here
        result = f"SecondTask executed with params: {self.params}"
        return result
