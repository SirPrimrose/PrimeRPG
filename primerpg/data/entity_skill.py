#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

from primerpg.util import level_from_total_xp, progress_to_next_level, req_xp_for_level


class EntitySkill:
    def __init__(self, entity_id: int, skill_id: int, total_xp: int):
        self.entity_id = entity_id
        self.skill_id = skill_id
        self._total_xp = total_xp
        self._level = self._calculate_level()

    def __repr__(self):
        var_text = " ".join(["{0}={1!r}".format(var, value) for var, value in vars(self).items()])
        return "<{0.__class__.__name__} {1}>".format(self, var_text)

    def get_total_xp(self):
        return self._total_xp

    def get_level(self):
        return self._level

    def modify_xp(self, xp_delta):
        new_xp = self._total_xp + xp_delta
        self._set_xp(new_xp)

    def set_level(self, new_level):
        new_xp = req_xp_for_level(new_level)
        self._set_xp(new_xp)

    def progress_to_next_level(self):
        return progress_to_next_level(self._total_xp)

    def _calculate_level(self):
        return level_from_total_xp(self._total_xp)

    def _set_xp(self, new_xp):
        self._total_xp = max(new_xp, 0)
        self._level = self._calculate_level()
