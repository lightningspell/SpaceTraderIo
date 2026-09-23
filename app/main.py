from dotenv import load_dotenv
load_dotenv()  # liest .env aus dem aktuellen Arbeitsverzeichnis und setzt os.environ

import os
import database_handler as db_handler
import api_interaction as api
from spaceTraderClasses import *

print("Hello World!")

if __name__ == "__main__":
    #Just a test to see if the SpaceTraderAPI class works correctly.
    # reset = api.api_get_reset_info()
    # print(reset.reset_id)
    # factions= api.get_all_factions(os.getenv("SPACETRADER_ACCOUNT_KEY"))
    # faction = factions[0]
    # print(faction.name)
    agent: Agent = api.create_agent("asdxcr")
    print(agent.agent_token)


    