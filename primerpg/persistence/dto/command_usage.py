#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm


class CommandUsage:
    def __init__(self, player_id: int, command_id: int, time_last_used: str):
        self.player_id = player_id
        self.command_id = command_id
        self.time_last_used = time_last_used

    def __repr__(self):
        var_text = " ".join(["{0}={1!r}".format(var, value) for var, value in vars(self).items()])
        return "<{0.__class__.__name__} {1}>".format(self, var_text)
