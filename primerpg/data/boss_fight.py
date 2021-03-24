#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm
from random import random

from primerpg.data.boss_profile import BossProfile
from primerpg.data.fight_log.fight_log import FightLog
from primerpg.data.fight_log.message_action import MessageAction
from primerpg.data.fight_log.turn_action import TurnAction
from primerpg.data.player_profile import PlayerProfile
from primerpg.helpers.moveset_helper import get_all_move_ids
from primerpg.helpers.recon_helper import get_variance, get_damage
from primerpg.helpers.stat_helper import get_total_scaled_stat_value
from primerpg.persistence.dto.move import Move
from primerpg.persistence.move_persistence import get_move


class BossFight:
    def __init__(self, player_profile: PlayerProfile, boss_profile: BossProfile):
        self.player_profile = player_profile
        self.boss_profile = boss_profile
        self.fighter_moves = [get_move(move_id) for move_id in get_all_move_ids(player_profile)]
        self.enemy_moves = [get_move(move_id) for move_id in get_all_move_ids(boss_profile)]
        self.turn = 0
        self.log = FightLog()

    def player_use_move(self, move: Move):
        if random() < move.success_chance:
            attack_value = get_total_scaled_stat_value(
                move.scaling_equipment_stat_id, self.player_profile.skills, self.player_profile.equipment
            )
            armor_value = get_total_scaled_stat_value(
                move.armor_equipment_stat_id, self.player_profile.skills, self.player_profile.equipment
            )
            scaled_move_attack = attack_value * move.power / 50.0
            if move.damage_type_id in self.boss_profile.type_strength_ids:
                scaled_move_attack /= 2
            if move.damage_type_id in self.boss_profile.type_weakness_ids:
                scaled_move_attack *= 1.5
            attack_power_mod = get_variance() * scaled_move_attack
            damage = get_damage(attack_power_mod, armor_value)

            self.log.add_action(MessageAction("Player damaged boss for {}".format(damage)))
            self.boss_profile.change_current_hp(-damage)
        else:
            # Missed the attack, roll for miss effect
            self.log.add_action(MessageAction("Player missed boss"))
            pass

    def boss_use_move(self):
        self.player_profile.change_current_hp(-1)
        self.log.add_action(MessageAction("Boss damaged player for {}".format(1)))

    def take_full_turn(self, player_move):
        self.log.add_action(TurnAction(self.turn))
        self.turn += 1

        self.player_use_move(player_move)
        self.boss_use_move()
