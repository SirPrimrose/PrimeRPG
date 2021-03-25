#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

from random import random, randrange
from typing import Optional

from primerpg.data.boss_profile import BossProfile
from primerpg.data.entity_base import EntityBase
from primerpg.data.fight_log.bossfight_action import BossfightAction
from primerpg.data.fight_log.fight_log import FightLog
from primerpg.data.fight_log.message_action import MessageAction
from primerpg.data.fight_log.turn_action import TurnAction
from primerpg.data.player_profile import PlayerProfile
from primerpg.helpers.moveset_helper import get_all_move_ids
from primerpg.helpers.recon_helper import get_variance, get_damage
from primerpg.helpers.stat_helper import get_total_scaled_stat_value
from primerpg.persistence.dto.move import Move
from primerpg.persistence.move_persistence import get_move

_turn_limit = 100
_power_divider = 20


class BossFight:
    def __init__(self, player_profile: PlayerProfile, boss_profile: BossProfile):
        self.player_profile = player_profile
        self.boss_profile = boss_profile
        self.player_moves = [get_move(move_id) for move_id in get_all_move_ids(player_profile)]
        self.boss_moves = [get_move(move_id) for move_id in get_all_move_ids(boss_profile)]
        self.turn = 0
        self.fight_log = FightLog()

    def use_move(self, move: Move, attacker: EntityBase, defender: EntityBase):
        hit_successes = 0
        for i in range(move.hits):
            if random() < move.success_chance:
                hit_successes += 1
        if hit_successes > 0:
            damage = 0
            attack_value = get_total_scaled_stat_value(
                move.scaling_equipment_stat_id, attacker.skills, attacker.equipment
            )
            armor_value = get_total_scaled_stat_value(move.armor_equipment_stat_id, defender.skills, defender.equipment)
            for hit in range(hit_successes):
                attack_mod = get_variance() * attack_value
                damage += get_damage(attack_mod, armor_value)
            power_damage = damage * move.power / _power_divider
            not_effective = False
            super_effective = False
            if type(defender) is BossProfile:
                if move.damage_type_id in defender.type_strength_ids:
                    power_damage /= 2
                    not_effective = True
                if move.damage_type_id in defender.type_weakness_ids:
                    power_damage *= 2
                    super_effective = True

            defender.change_current_hp(-power_damage)
            self.fight_log.add_action(
                BossfightAction(
                    attacker_name=attacker.name,
                    defender_name=defender.name,
                    damage=power_damage,
                    multi_hit=hit_successes if move.hits > 1 else None,
                    move_name=move.name,
                    super_effective=super_effective,
                    not_effective=not_effective,
                )
            )
        else:
            # Missed the attack, roll for miss effect
            self.fight_log.add_action(MessageAction("{} missed {}".format(attacker.name, defender.name)))
            pass

    def get_random_boss_move(self) -> Move:
        return self.boss_moves[randrange(len(self.boss_moves))]

    def get_random_player_move(self) -> Move:
        return self.player_moves[randrange(len(self.player_moves))]

    def take_full_turn(self, player_move: Optional[Move]):
        self.fight_log.add_action(TurnAction(self.turn))
        self.turn += 1
        if not player_move:
            player_move = self.get_random_player_move()
            self.fight_log.add_action(MessageAction("{} used random move".format(self.player_profile.name)))

        self.use_move(player_move, self.player_profile, self.boss_profile)
        self.use_move(self.get_random_boss_move(), self.boss_profile, self.player_profile)

    def is_fight_done(self):
        return self.player_profile.is_dead() or self.boss_profile.is_dead() or self.turn >= _turn_limit
