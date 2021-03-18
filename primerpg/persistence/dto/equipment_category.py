#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm


class EquipmentCategory:
    def __init__(self, unique_id: int, name: str, max_num: int):
        self.unique_id = unique_id
        self.name = name
        self.max_num = max_num

    def __repr__(self):
        response = "Unique Id: %s" % self.unique_id
        response += "\nName: %s" % self.name
        response += "\nMaximum Number: %s" % self.max_num
        return response
