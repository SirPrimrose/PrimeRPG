#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm


class PlayerCore:
    def __init__(
        self,
        unique_id: int,
        name: str,
        avatar_url: str,
        state_id: int,
        zone_id: int,
        current_hp: float,
        hp_regen: float,
    ):
        self.unique_id = unique_id
        self.name = name
        self.avatar_url = avatar_url
        # TODO Update state to state_id
        self.state_id = state_id
        self.zone_id = zone_id
        self.current_hp = current_hp
        self.hp_regen = hp_regen

    def __repr__(self):
        response = "Unique Id: %s" % self.unique_id
        response += "\nName: %s" % self.name
        response += "\nAvatar URL: %s" % self.avatar_url
        response += "\nState Id: %s" % self.state_id
        response += "\nZone Id: %s" % self.zone_id
        response += "\nCurrent HP: %s" % self.current_hp
        response += "\nHP Regen: %s" % self.hp_regen
        return response
