#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm


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
        var_text = " ".join(["{0}={1!r}".format(var, value) for var, value in vars(self).items()])
        return "<{0.__class__.__name__} {1}>".format(self, var_text)
