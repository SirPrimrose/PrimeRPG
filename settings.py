#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Snack

import os

from dotenv import load_dotenv


def env_setup():
    # Will be run on app setup to ensure .env is found before loading
    # Reformat if .env & db structure will be on a dedicated server for those services
    load_dotenv(override=True)


def get_env_var(var_name: str):
    return os.getenv(var_name)
