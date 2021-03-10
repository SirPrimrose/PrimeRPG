import math
import random

from consts import speed_skill_id, luck_skill_id
from data.entity_base import EntityBase

attack_variance = 0.3
crit_divider = 50
crit_cap = 0.4  # percent
dodge_spd_divider = 5
dodge_lck_divider = 25
dodge_cap = 0.1  # percent


def get_damage(attack, armor):
    if attack > armor:
        damage = (
            0.60307 * armor + attack - 0.79 * armor * math.exp(-0.27 * armor / attack)
        )
        pass
    else:
        damage = (
            1 * (math.pow(attack, 3) / math.pow(armor, 2))
            - 0.09 * math.pow(attack, 2) / armor
            + 0.09 * attack
        )
        pass
    return round(max(damage, 1))


def sim_fight(attacker: EntityBase, defender: EntityBase):
    """Simulates a fight between two StatEntity objects

    :param attacker:
    :param defender:
    :return: The winner of the fight
    """
    turn = 0
    while turn < 100:
        print("Turn {}:".format(turn))
        if attacker.is_dead():
            print("{} won!".format(defender.name))
            return defender
        if defender.is_dead():
            print("{} won!".format(attacker.name))
            return attacker
        process_turn(attacker, defender)
        process_turn(defender, attacker)
        turn += 1


def process_turn(attacker: EntityBase, defender: EntityBase):
    if attacker.is_dead():
        return
    else:
        print(process_attack(attacker, defender))
        if random.random() < get_double_attack_chance(attacker, defender):
            print("Double attack for {}!".format(attacker.name))
            print(process_attack(attacker, defender))


def process_attack(attacker: EntityBase, defender: EntityBase):
    modified_attack = get_variance() * attacker.get_attack_power()

    attacker_luck = attacker.get_skill_value(luck_skill_id).level
    defender_luck = attacker.get_skill_value(luck_skill_id).level
    attacker_speed = attacker.get_skill_value(speed_skill_id).level
    defender_speed = attacker.get_skill_value(speed_skill_id).level
    crit = random.random() < get_crit_chance(attacker_luck)

    response = ""
    if crit:
        damage = get_damage(modified_attack, 0)
        response += "Crit! "
    else:
        dodge = random.random() < get_dodge_chance(
            attacker_speed, defender_speed, defender_luck
        )
        if dodge:
            response += "Dodged! "
            damage = 0
        else:
            damage = get_damage(modified_attack, defender.get_armor_power())

    defender.current_hp -= damage
    response += "{0} dealt {1:.2f} damage to {2}. {2} has {3:.2f} hp remaining.".format(
        attacker.name, damage, defender.name, defender.current_hp
    )
    return response


def get_variance():
    return 1 + random.random() * attack_variance - attack_variance / 2


def get_crit_chance(luck):
    return math.tanh(luck / crit_divider) * crit_cap


def get_double_attack_chance(attacker, defender):
    attacker_speed = attacker.get_skill_value(speed_skill_id).level
    defender_speed = defender.get_skill_value(speed_skill_id).level
    return (attacker_speed - defender_speed) * 0.1


# Dependent on both attacker's speed, defender's speed, and defender's luck
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
