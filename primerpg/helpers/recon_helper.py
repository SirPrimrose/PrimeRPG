#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

import math
import random

from primerpg.consts import speed_skill_id, luck_skill_id, skill_ids
from primerpg.data.entity_base import EntityBase
from primerpg.data.fight_log.damage_action import DamageAction
from primerpg.data.fight_log.effort_action import EffortAction
from primerpg.data.fight_log.fight_log import FightLog, Effort
from primerpg.data.fight_log.message_action import MessageAction
from primerpg.data.fight_log.turn_action import TurnAction
from primerpg.data.mob_profile import MobProfile
from primerpg.data.player_profile import PlayerProfile
from primerpg.data.weighted_value import WeightedValue
from primerpg.helpers.item_helper import give_player_item
from primerpg.helpers.mob_helper import get_mob_kill_rewards
from primerpg.helpers.player_helper import apply_death_penalty
from primerpg.util import get_random_from_weighted_list

attack_variance = 0.3
crit_divider = 50
crit_cap = 0.4  # percent
dodge_spd_divider = 5
dodge_lck_divider = 25
dodge_cap = 0.1  # percent
double_attack_per_speed_level = 0.05
min_effort_chance = 0.05
max_effort_chance = 0.5
_turn_limit = 100


# TODO Refactor all methods specific to the recon fight into a ReconFight object, leave all damage and
# TODO stat calculations here in battle helper
def get_damage(attack, armor) -> float:
    if attack <= 0:
        return 0
    if armor > 8 * attack:
        damage = 0.1 * attack
    elif armor > attack:
        damage = (19.2 / 49 * math.pow(attack / armor - 0.125, 2) + 0.1) * attack
    elif armor > 0.4 * attack:
        damage = (-0.4 / 3 * math.pow(attack / armor - 2.5, 2) + 0.7) * attack
    elif armor > 0.125 * attack:
        damage = (-0.8 / 121 * math.pow(attack / armor - 8, 2) + 0.9) * attack
    else:
        damage = 0.9 * attack
    return max(damage, 1)


def credit_effort(attacker: EntityBase, log: FightLog):
    for effort in log.get_efforts():
        attacker.give_skill_effort(effort.skill_id, effort.value)


def player_lose(attacker: PlayerProfile, defender: MobProfile, log: FightLog):
    log.add_action(MessageAction("{} won!".format(defender.name)))
    log.add_action(MessageAction("{} died and lost 50% of each skill level (above level 5)".format(attacker.name)))
    apply_death_penalty(attacker)


def player_win(attacker: PlayerProfile, defender: MobProfile, log: FightLog):
    log.add_action(MessageAction("{} won!".format(attacker.name)))
    credit_effort(attacker, log)
    log.add_rewards(get_mob_kill_rewards(defender))
    for reward in log.get_rewards():
        give_player_item(attacker, reward)


def sim_recon_fight(attacker: EntityBase, defender: EntityBase) -> FightLog:
    """Simulates a fight between two EntityBase objects

    :param attacker:
    :param defender:
    :return: A log of the fight results
    """
    log = FightLog()
    turn = 0
    while turn < _turn_limit:
        log.add_action(TurnAction(turn))
        if attacker.is_dead():
            player_lose(attacker, defender, log)
            return log
        if defender.is_dead():
            player_win(attacker, defender, log)
            return log
        if defender.get_skill_level(speed_skill_id) <= attacker.get_skill_level(speed_skill_id):
            process_turn(attacker, defender, log)
            process_turn(defender, attacker, log)
        else:
            process_turn(defender, attacker, log)
            process_turn(attacker, defender, log)
        turn += 1
    return log


def process_turn(attacker: EntityBase, defender: EntityBase, log: FightLog):
    if attacker.is_dead():
        return
    else:
        process_attack(attacker, defender, log)
        if random.random() < get_double_attack_chance(attacker, defender):
            log.add_action(MessageAction("Double attack for {}!".format(attacker.name)))
            process_attack(attacker, defender, log)


def process_attack(attacker: EntityBase, defender: EntityBase, log: FightLog):
    var = get_variance()
    mod_phys_attack = var * attacker.get_phys_atk_power()
    mod_mag_attack = var * attacker.get_mag_atk_power()

    attacker_luck = attacker.get_skill_level(luck_skill_id)
    defender_luck = attacker.get_skill_level(luck_skill_id)
    attacker_speed = attacker.get_skill_level(speed_skill_id)
    defender_speed = attacker.get_skill_level(speed_skill_id)
    crit = random.random() < get_crit_chance(attacker_luck)
    dodge = False

    response = ""
    if crit:
        phys_damage = get_damage(mod_phys_attack * 1.5, defender.get_phys_arm_power() / 2)
        mag_damage = get_damage(mod_mag_attack * 1.5, defender.get_mag_arm_power() / 2)
    else:
        dodge = random.random() < get_dodge_chance(attacker_speed, defender_speed, defender_luck)
        if dodge:
            phys_damage = 0.0
            mag_damage = 0.0
        else:
            phys_damage = get_damage(mod_phys_attack, defender.get_phys_arm_power())
            mag_damage = get_damage(mod_mag_attack, defender.get_mag_arm_power())

    total_damage = phys_damage + mag_damage
    defender.change_current_hp(-total_damage)
    is_player = isinstance(attacker, PlayerProfile)
    log.add_action(
        DamageAction(
            attacker_name=attacker.name,
            defender_name=defender.name,
            defender_hp=defender.get_current_hp(),
            damage=total_damage,
            player_attacking=is_player,
            crit=crit,
            dodge=dodge,
        )
    )
    if is_player:
        def_cb = defender.get_combat_level()
        atk_cb = attacker.get_combat_level()
        if random.random() < get_effort_chance(atk_cb, def_cb):
            weighted_skills = [WeightedValue(defender.get_skill_level(skill_id), skill_id) for skill_id in skill_ids]
            effort_skill_id: WeightedValue = get_random_from_weighted_list(weighted_skills)
            effort_value = (random.random() + 0.5) * total_damage * get_effort_multiplier()
            effort = Effort(effort_skill_id.value, int(effort_value))
            log.add_effort(effort)
            log.add_action(EffortAction(effort))
    return response


def get_effort_multiplier():
    return 5


def get_effort_chance(attacker_cb: int, defender_cb: int):
    diff = (defender_cb - attacker_cb) + 14
    if diff <= 0:
        return min_effort_chance
    return min(min_effort_chance + 0.025 * diff, max_effort_chance)


def get_variance():
    return 1 + random.random() * attack_variance - attack_variance / 2


def get_crit_chance(luck):
    return math.tanh(luck / crit_divider) * crit_cap


def get_double_attack_chance(attacker, defender):
    attacker_speed = attacker.get_skill_level(speed_skill_id)
    defender_speed = defender.get_skill_level(speed_skill_id)
    return (attacker_speed - defender_speed) * double_attack_per_speed_level


def get_dodge_chance(atk_spd, def_spd, def_lck):
    return (
        math.tanh(max(def_spd - atk_spd, 0) / dodge_spd_divider) * dodge_cap
        + math.tanh(def_lck / dodge_lck_divider) * dodge_cap
    )


def get_flee_chance(fighter_speed: int, enemy_speed: int) -> float:
    if enemy_speed <= 0:
        return 1.0
    speed_ratio = fighter_speed / enemy_speed
    return min(max(speed_ratio + (1 / 8) * (1 - speed_ratio), 0.0), 1.0)
