class Fish:
    def __init__(
        self,
        unique_id: int,
        item_id: int,
        name: str,
        start_time: str,
        end_time: str,
        weather: str,
        weight: int,
    ):
        self.unique_id = unique_id
        self.item_id = item_id
        self.name = name
        self.start_time = start_time
        self.end_time = end_time
        self.weather = weather
        self.weight = weight

    def __repr__(self):
        response = "Unique Id: %s" % self.unique_id
        response += "\nItem Id: %s" % self.item_id
        response += "\nName: %s" % self.name
        response += "\nStart Time: %s" % self.start_time
        response += "\nEnd Time: %s" % self.end_time
        response += "\nWeather: %s" % self.weather
        response += "\nWeight: %s" % self.weight
        return response
