#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

from primerpg.data.fight_log.fight_log import FightLog
from primerpg.data.fight_log.turn_action import TurnAction
from primerpg.embeds.simple_embed import SimpleEmbed


async def print_log(channel, fight_log: FightLog):
    response = ""
    current_turn = ""
    page_num = 1

    async def check_add_turn_to_response():
        nonlocal response, current_turn, page_num
        if len(response) + len(current_turn) >= 2048:
            await send_fight_log_page(channel, page_num, response)
            page_num += 1
            response = ""
        response += current_turn
        current_turn = ""

    for log in fight_log.actions:
        if type(log) == TurnAction:
            await check_add_turn_to_response()
        current_turn += "\n" if log.newline else ""
        current_turn += "{}".format(log.get_message())
    await check_add_turn_to_response()

    await send_fight_log_page(channel, page_num, response, page_num != 1)


async def send_fight_log_page(channel, page_num, content, show_page_num=True):
    title = "Fight Log Page {}".format(page_num) if show_page_num else "Fight Log"
    embed = SimpleEmbed(None, title, content)
    await channel.send(embed=embed.generate_embed())
