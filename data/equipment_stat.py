class EquipmentStat:
    def __init__(
        self,
        item_id: int,
        equipment_stat_category_id: int,
        value: int,
        scales_with: dict,
    ):
        self.item_id = item_id
        self.equipment_stat_category_id = equipment_stat_category_id
        self.value = value
        self.scales_with = scales_with

    def __repr__(self):
        response = "Item Id: %s" % self.item_id
        response += "\nEquipment Stat Category Id: %s" % self.equipment_stat_category_id
        response += "\nValue: %s" % self.value
        response += "\nScaling: %s" % self.scales_with
        return response
