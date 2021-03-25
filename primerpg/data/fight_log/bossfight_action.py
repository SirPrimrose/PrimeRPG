#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

from primerpg.data.fight_log.action_base import ActionBase
from primerpg.emojis import (
    emoji_from_id,
    damage_emoji_id,
    attack_emoji_id,
    super_effective_emoji_id,
    not_effective_emoji_id,
)


class BossfightAction(ActionBase):
    def __init__(
        self,
        attacker_name: str,
        defender_name: str,
        damage: float,
        move_name: str,
        super_effective: bool = False,
        not_effective: bool = False,
        multi_hit: int = None,
    ):
        super().__init__()
        self.attacker_name = attacker_name
        self.defender_name = defender_name
        self.damage = damage
        self.move_name = move_name
        self.super_effective = super_effective
        self.not_effective = not_effective
        self.multi_hit = multi_hit

    def get_message(self) -> str:
        multi_hit_text = "(hit {}x)".format(self.multi_hit) if self.multi_hit else ""
        move_text = "used {}".format(self.move_name) if self.move_name else ""
        return "{0} {1}{2} on {4} for **{5:.0f}**{6}".format(
            self.attacker_name,
            move_text,
            multi_hit_text,
            emoji_from_id(attack_emoji_id),
            self.defender_name,
            self.damage,
            emoji_from_id(self.get_damage_icon()),
        )

    def get_damage_icon(self) -> int:
        if self.super_effective:
            return super_effective_emoji_id
        if self.not_effective:
            return not_effective_emoji_id
        return damage_emoji_id
