class PlayerTaskCore:
    def __init__(
        self,
        player_id: int,
        task_id: int,
        time_started: str,
    ):
        self.player_id = player_id
        self.task_id = task_id
        self.time_started = time_started

    def __repr__(self):
        response = "Unique ID: %s" % self.player_id
        response += "\nTask ID: %s" % self.task_id
        response += "\nTime Started: %s" % self.time_started
        return response
