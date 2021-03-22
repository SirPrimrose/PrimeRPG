#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm


class MobCore:
    def __init__(
        self,
        unique_id: int,
        name: str,
        weight: int,
        icon_url: str,
    ):
        self.unique_id = unique_id
        self.name = name
        self.weight = weight
        self.icon_url = icon_url

    def __repr__(self):
        response = "Unique ID: %s" % self.unique_id
        response += "\nName: %s" % self.name
        response += "\nWight: %s" % self.weight
        response += "\nIcon URL: %s" % self.icon_url
        return response
