#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm


class SkillCategory:
    def __init__(self, unique_id: int, name: str, short_name: str):
        self.unique_id = unique_id
        self.name = name
        self.short_name = short_name

    def __repr__(self):
        response = "Unique Id: %s" % self.unique_id
        response += "\nName: %s" % self.name
        response += "\nShort Name: %s" % self.short_name
        return response
