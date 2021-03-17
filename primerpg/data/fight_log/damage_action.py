from primerpg.data.fight_log.action_base import ActionBase
from primerpg.emojis import (
    player_heart_id,
    enemy_heart_id,
    emoji_from_id,
    damage_emoji_id,
    attack_emoji_id,
)


class DamageAction(ActionBase):
    def __init__(
        self,
        attacker_name: str,
        defender_name: str,
        defender_hp: float,
        damage: int,
        player_attacking: bool,
    ):
        super().__init__()
        self.attacker_name = attacker_name
        self.defender_name = defender_name
        self.defender_hp = defender_hp
        self.damage = damage
        self.player_attacking = player_attacking

    def get_message(self):
        heart = enemy_heart_id if self.player_attacking else player_heart_id
        return "{0} {1} {2} (**{3}** {4}) for **{5}**{6}".format(
            self.attacker_name,
            emoji_from_id(attack_emoji_id),
            self.defender_name,
            self.defender_hp,
            emoji_from_id(heart),
            self.damage,
            emoji_from_id(damage_emoji_id),
        )
