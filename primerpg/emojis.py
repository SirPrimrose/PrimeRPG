#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

from typing import Dict

from primerpg import consts
from primerpg.consts import fishing_task_id, farming_task_id, foraging_task_id, woodcutting_task_id, mining_task_id

vitality_emoji_id = 821118647766482955
strength_emoji_id = 821118786446950420
dexterity_emoji_id = 821118535001440258
defense_emoji_id = 821118524423929897
intellect_emoji_id = 821118658892791828
faith_emoji_id = 821118564157095946
resistance_emoji_id = 821118696436924416
speed_emoji_id = 821118763126620191
luck_emoji_id = 821118673464066148

player_heart_id = 821118685301309481
enemy_heart_id = 821118551309025400
fight_emoji_id = 821118492849340477
heal_emoji_id = 821118619651276852
run_emoji_id = 821118763126620191
info_emoji_id = 822280408653234238
attack_emoji_id = 821118492849340477
damage_emoji_id = 821118509526286356
crit_emoji_id = 822281781285617756
dodge_emoji_id = 822282292730527745
turn_emoji = ":arrows_counterclockwise:"

letter_s_low_emoji_id = 821118141815848960
letter_s_med_emoji_id = 821118123741806633
letter_s_high_emoji_id = 821118107850506300
letter_a_low_emoji_id = 821118212028366849
letter_a_med_emoji_id = 821118191039807519
letter_a_high_emoji_id = 821118167857365002
letter_b_low_emoji_id = 821118256298983425
letter_b_med_emoji_id = 821118242961621062
letter_b_high_emoji_id = 821118230079995904
letter_c_low_emoji_id = 821118299709636609
letter_c_med_emoji_id = 821118287748399153
letter_c_high_emoji_id = 821118274796126229
letter_d_low_emoji_id = 821118341238358076
letter_d_med_emoji_id = 821118329359695872
letter_d_high_emoji_id = 821118313265758238
letter_e_low_emoji_id = 821118379087233115
letter_e_med_emoji_id = 821118366563172382
letter_e_high_emoji_id = 821118354882166804
letter_f_low_emoji_id = 821118418194923541
letter_f_med_emoji_id = 821118407540736052
letter_f_high_emoji_id = 821118395331248198

skill_emojis: Dict[int, int] = {
    vitality_emoji_id: consts.vitality_skill_id,
    strength_emoji_id: consts.strength_skill_id,
    dexterity_emoji_id: consts.dexterity_skill_id,
    intellect_emoji_id: consts.intellect_skill_id,
    faith_emoji_id: consts.faith_skill_id,
    luck_emoji_id: consts.luck_skill_id,
    defense_emoji_id: consts.defense_skill_id,
    resistance_emoji_id: consts.resistance_skill_id,
    speed_emoji_id: consts.speed_skill_id,
}

grade_emojis: Dict[int, int] = {
    3: letter_f_low_emoji_id,
    6: letter_f_med_emoji_id,
    10: letter_f_high_emoji_id,
    13: letter_e_low_emoji_id,
    16: letter_e_med_emoji_id,
    20: letter_e_high_emoji_id,
    23: letter_d_low_emoji_id,
    26: letter_d_med_emoji_id,
    30: letter_d_high_emoji_id,
    33: letter_c_low_emoji_id,
    36: letter_c_med_emoji_id,
    40: letter_c_high_emoji_id,
    43: letter_b_low_emoji_id,
    46: letter_b_med_emoji_id,
    50: letter_b_high_emoji_id,
    53: letter_a_low_emoji_id,
    56: letter_a_med_emoji_id,
    60: letter_a_high_emoji_id,
    63: letter_s_low_emoji_id,
    66: letter_s_med_emoji_id,
    70: letter_s_high_emoji_id,
}

task_emojis: Dict[int, int] = {
    fishing_task_id: letter_s_high_emoji_id,
    mining_task_id: letter_a_high_emoji_id,
    woodcutting_task_id: letter_b_high_emoji_id,
    foraging_task_id: letter_c_high_emoji_id,
    farming_task_id: letter_d_high_emoji_id,
}


def emoji_from_id(emoji_id: int) -> str:
    return "<:z:{}>".format(emoji_id)


def extract_id_from_emoji(emoji_text: str) -> int:
    """Finds the id in an emoji str that follows the format <:name:id>

    :param emoji_text: The text representation of the emoji
    :return: The id of the emoji, or 0 if the id was not found
    """
    start = emoji_text.rfind(":") + 1
    end = emoji_text.rfind(">")
    try:
        return int(emoji_text[start:end])
    except ValueError:
        return 0
