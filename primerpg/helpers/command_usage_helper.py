#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm
import datetime

from primerpg.data_cache import get_command_requirement_by_name
from primerpg.date_util import date_from_str, time_since, str_from_date, time_delta_to_readable_str
from primerpg.persistence.command_usage_persistence import get_command_usage, update_command_usage, insert_command_usage
from primerpg.persistence.dto.command_requirement import CommandRequirement
from primerpg.persistence.dto.command_usage import CommandUsage


def is_command_off_cooldown(player_id: int, command_req: CommandRequirement):
    if command_req.cooldown <= 0:
        return True, ""

    usage = get_command_usage(player_id, command_req.unique_id)
    if usage:
        delta_time_since = time_since(date_from_str(usage.time_last_used))
        delta_cooldown = datetime.timedelta(seconds=command_req.cooldown)
        cooldown_left = delta_cooldown - delta_time_since
        if cooldown_left.total_seconds() <= 0:
            return True, ""
        else:
            return False, "Command is still on cooldown. Remaining time: `{}`".format(
                time_delta_to_readable_str(cooldown_left)
            )
    else:
        return True, ""


def set_command_last_usage(player_id: int, command_name: str):
    command_req = get_command_requirement_by_name(command_name)
    if not command_req or command_req.cooldown <= 0:
        return

    new_usage = CommandUsage(player_id, command_req.unique_id, str_from_date(datetime.datetime.utcnow()))
    current_usage = get_command_usage(player_id, command_req.unique_id)
    if current_usage:
        update_command_usage(new_usage)
    else:
        insert_command_usage(new_usage)
