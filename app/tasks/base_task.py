
class BaseTask:
    def __init__(self, params):
        self.params = params
        self.description = "No Description Provided!"
        self.inputs = []
        self.file_upload = False

    def run(self):
        raise NotImplementedError("This function should be implemented in the subclasses.")

    def get_input_config(self):
        return {
            "inputs": self.inputs,
            "fileUpload": self.file_upload
        }
