#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm


class CommandUsage:
    def __init__(self, player_id: int, command_id: int, time_last_used: str):
        self.player_id = player_id
        self.command_id = command_id
        self.time_last_used = time_last_used

    def __repr__(self):
        response = "Player Id: %s" % self.player_id
        response += "\nCommand Id: %s" % self.command_id
        response += "\nTime Last Used: %s" % self.time_last_used
        return response
