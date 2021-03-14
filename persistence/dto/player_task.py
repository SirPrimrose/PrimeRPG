class PlayerTask:
    def __init__(
        self,
        player_id: int,
        task: str,
        time_started: str,
    ):
        self.player_id = player_id
        self.task = task
        self.time_started = time_started

    def __repr__(self):
        response = "Unique ID: %s" % self.player_id
        response += "\nTask Name: %s" % self.task
        response += "\nTime Started: %s" % self.time_started
        return response
