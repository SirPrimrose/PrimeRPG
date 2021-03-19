#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm


class ShopItem:
    def __init__(self, item_id: int, cost: int, zone_id: int):
        self.item_id = item_id
        self.cost = cost
        self.zone_id = zone_id
