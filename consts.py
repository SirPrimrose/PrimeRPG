from pathlib import Path

import discord

command_prefix = "."
game_client = discord.Client()

# Game Vars
day_night_cycles_per_day = 6
weather_frequency = 6000  # seconds
base_fish_frequency = 1  # seconds

# Tasks
fishing_task = "fishing"
mining_task = "mining"
woodcutting_task = "woodcutting"
foraging_task = "foraging"

# Weather
raining_weather = "raining"
clear_weather = "clear"

# Folders
data_folder = Path("data/raw_data")

# Skill ids
health_skill_id = 1
strength_skill_id = 2
dexterity_skill_id = 3
defense_skill_id = 4
intellect_skill_id = 5
faith_skill_id = 6
resistance_skill_id = 7
speed_skill_id = 8
luck_skill_id = 9

# Equipment Stat ids
attack_stat_id = 1
armor_stat_id = 2
