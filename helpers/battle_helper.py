import math
import random

from consts import speed_skill_id, luck_skill_id, skill_ids
from data.entity_base import EntityBase
from data.fight_log.damage_action import DamageAction
from data.fight_log.effort_action import EffortAction
from data.fight_log.fight_log import FightLog, Effort
from data.fight_log.message_action import MessageAction
from data.fight_log.turn_action import TurnAction
from data.mob_profile import MobProfile
from data.player_profile import PlayerProfile
from data.weighted_value import WeightedValue
from helpers.item_helper import give_player_item
from helpers.mob_helper import get_mob_kill_rewards
from helpers.player_helper import apply_death_penalty
from util import get_random_from_weighted_table

attack_variance = 0.3
crit_divider = 50
crit_cap = 0.4  # percent
dodge_spd_divider = 5
dodge_lck_divider = 25
dodge_cap = 0.1  # percent
double_attack_per_speed_level = 0.05
min_effort_chance = 0.05
max_effort_chance = 0.5


# TODO Refactor all methods specific to the recon fight into a ReconFight object, leave all damage and
# TODO stat calculations here in battle helper
def get_damage(attack, armor):
    if attack > armor:
        damage = (
            0.60307 * armor + attack - 0.79 * armor * math.exp(-0.27 * armor / attack)
        )
    else:
        damage = (
            1 * (math.pow(attack, 3) / math.pow(armor, 2))
            - 0.09 * math.pow(attack, 2) / armor
            + 0.09 * attack
        )
    return round(max(damage, 1))


def credit_effort(attacker: EntityBase, log: FightLog):
    for effort in log.efforts:
        attacker.give_skill_effort(effort.skill_id, effort.value)


def player_lose(attacker: PlayerProfile, defender: MobProfile, log: FightLog):
    log.add_action(MessageAction("{} won!".format(defender.name)))
    log.add_action(
        MessageAction(
            "{} died and lost 50% of each skill level (above level 5)".format(
                attacker.name
            )
        )
    )
    apply_death_penalty(attacker)


def player_win(attacker: PlayerProfile, defender: MobProfile, log: FightLog):
    log.add_action(MessageAction("{} won!".format(attacker.name)))
    credit_effort(attacker, log)
    log.add_rewards(get_mob_kill_rewards(defender))
    for reward in log.get_rewards():
        give_player_item(attacker, reward)


def sim_fight(attacker: EntityBase, defender: EntityBase) -> FightLog:
    """Simulates a fight between two EntityBase objects

    :param attacker:
    :param defender:
    :return: The winner of the fight
    """
    log = FightLog()
    turn = 0
    while turn < 100:
        log.add_action(TurnAction(turn))
        if attacker.is_dead():
            player_lose(attacker, defender, log)
            return log
        if defender.is_dead():
            player_win(attacker, defender, log)
            return log
        if defender.get_skill_level(speed_skill_id) <= attacker.get_skill_level(
            speed_skill_id
        ):
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

    response = ""
    if crit:
        # TODO Add a Crit Action
        phys_damage = get_damage(mod_phys_attack, 0)
        mag_damage = get_damage(mod_mag_attack, 0)
    else:
        dodge = random.random() < get_dodge_chance(
            attacker_speed, defender_speed, defender_luck
        )
        if dodge:
            # TODO Add a Dodged Action
            phys_damage = 0
            mag_damage = 0
        else:
            phys_damage = get_damage(mod_phys_attack, defender.get_phys_arm_power())
            mag_damage = get_damage(mod_mag_attack, defender.get_phys_arm_power())

    total_damage = phys_damage + mag_damage
    defender.change_current_hp(-total_damage)
    is_player = isinstance(attacker, PlayerProfile)
    log.add_action(
        DamageAction(
            attacker.name,
            defender.name,
            defender.get_current_hp(),
            total_damage,
            is_player,
        )
    )
    if is_player:
        def_cb = defender.get_combat_level()
        atk_cb = attacker.get_combat_level()
        if random.random() < get_effort_chance(atk_cb, def_cb, total_damage):
            weighted_skills = [
                WeightedValue(defender.get_skill_level(skill_id) + 1, skill_id)
                for skill_id in skill_ids
            ]
            effort_skill_id: WeightedValue = get_random_from_weighted_table(
                weighted_skills
            )
            effort_value = (
                (random.random() + 0.5) * total_damage * get_effort_multiplier()
            )
            effort = Effort(effort_skill_id.value, int(effort_value))
            log.add_effort(effort)
            log.add_action(EffortAction(effort))
    return response


def get_effort_multiplier():
    return 5


def get_effort_chance(attacker_cb: int, defender_cb: int, damage: int):
    diff = (defender_cb - attacker_cb) + 5
    if diff <= 0:
        return min_effort_chance
    if attacker_cb <= 0:
        return max_effort_chance
    return min(
        max(
            math.pow((diff * 5) / math.sqrt(attacker_cb), 0.7)
            * math.pow(damage, 0.333)
            / 100,
            min_effort_chance,
        ),
        max_effort_chance,
    )


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
