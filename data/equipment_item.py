from typing import List

from data.equipment_stat import EquipmentStat
from data.item import Item


class EquipmentItem(Item):
    def __init__(self, stats: List[EquipmentStat], *args):
        super().__init__(*args)
        self.stats = stats

    def __repr__(self):
        response = super.__repr__()
        response += "\nStats: %s" % self.stats
        return response
