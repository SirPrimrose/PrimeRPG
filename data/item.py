class Item:
    def __init__(self, unique_id: int, category_id: int, name: str, value: int):
        self.unique_id = unique_id
        self.category_id = category_id
        self.name = name
        self.value = value

    def __repr__(self):
        response = "Unique Id: %s" % self.unique_id
        response += "\nCategory Id: %s" % self.category_id
        response += "\nName: %s" % self.name
        response += "\nValue: %s" % self.value
        return response


3
