#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm
from primerpg.data_cache import get_item_name


class ShopItem:
    def __init__(self, item_id: int, cost: int, zone_id: int):
        self.item_id = item_id
        self.cost = cost
        self.zone_id = zone_id

    def get_name(self) -> str:
        return get_item_name(self.item_id)
