from dotenv import load_dotenv
load_dotenv()  # liest .env aus dem aktuellen Arbeitsverzeichnis und setzt os.environ

import os
import database_handler as db_handler
import api_interaction as api

print("Hello World!")

if __name__ == "__main__":
    # Just a test to see if the SpaceTraderAPI class works correctly.
    reset = api.api_get_reset_info()
    account_token = os.getenv("ACCOUNT_TOKEN")
    factions = api.get_all_factions(account_token)

    