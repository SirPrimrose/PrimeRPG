from typing import List

from data.entity_equipment import EntityEquipment
from data.entity_skill import EntitySkill
from persistence.dto.equipment_stat import EquipmentStat
from util import get_equipment_stat


def _apply_scaling(stat: EquipmentStat, skills: List[EntitySkill]) -> float:
    base_value = stat.value
    scaling_values = []
    for skill in skills:
        if skill.skill_id in stat.scales_with:
            scaling = stat.scales_with[skill.skill_id]
            scaling_values.append(base_value * scaling * (skill.get_level() / 100))

    return base_value + sum(scaling_values)


def get_total_scaled_stat_value(
    stat_id, skills: List[EntitySkill], equipment: List[EntityEquipment]
) -> float:
    total_value = 0.0
    for e in equipment:
        total_value += get_scaled_stat_value_for_item(e.item_id, stat_id, skills)

    return total_value


def get_scaled_stat_value_for_item(
    item_id: int, stat_id: int, skills: List[EntitySkill]
) -> float:
    stat = get_equipment_stat(item_id, stat_id)
    if stat:
        return _apply_scaling(stat, skills)
    else:
        return 0
