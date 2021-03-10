from data.fight_log.action_base import ActionBase
from emojis import player_heart, enemy_heart, attack_emoji, damage_emoji


class DamageAction(ActionBase):
    def __init__(
        self,
        attacker_name: str,
        defender_name: str,
        defender_hp: int,
        damage: int,
        player_attacking,
        *args
    ):
        super(ActionBase, self).__init__(*args)
        self.attacker_name = attacker_name
        self.defender_name = defender_name
        self.defender_hp = defender_hp
        self.damage = damage
        self.player_attacking = player_attacking

    def get_message(self):
        heart = enemy_heart if self.player_attacking else player_heart
        return "{0} {1} {2} (**{3}** {4}) for **{5}**{6}".format(
            self.attacker_name,
            attack_emoji,
            self.defender_name,
            self.defender_hp,
            heart,
            self.damage,
            damage_emoji,
        )
