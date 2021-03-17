class TaskCategory:
    def __init__(self, unique_id: int, name: str):
        self.unique_id = unique_id
        self.name = name

    def __repr__(self):
        response = "Unique Id: %s" % self.unique_id
        response += "\nName: %s" % self.name
        return response
