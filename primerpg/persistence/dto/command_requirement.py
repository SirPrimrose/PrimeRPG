#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm
from typing import List


class CommandRequirement:
    def __init__(self, unique_id: int, name: str, zone_id: int, allowed_state_ids: List[int]):
        self.unique_id = unique_id
        self.name = name
        self.zone_id = zone_id
        self.allowed_state_ids = allowed_state_ids

    def __repr__(self):
        response = "Unique Id: %s" % self.unique_id
        response += "\nName: %s" % self.name
        response += "\nZone Id: %s" % self.zone_id
        response += "\nAllowed State Ids: %s" % self.allowed_state_ids
        return response
