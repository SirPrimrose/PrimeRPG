#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Snack

import os

from dotenv import load_dotenv


def env_setup():
    # Will be run on app setup to ensure .env is found before loading
    # Reformat if .env & db structure will be on a dedicated server for those services
    load_dotenv()


# Very basic usage; Primitive call through main.py
# If desired define func & return all env variables if needed
bot_token = os.getenv("BOT_TOKEN")
