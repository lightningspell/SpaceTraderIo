from dotenv import load_dotenv
load_dotenv()  # liest .env aus dem aktuellen Arbeitsverzeichnis und setzt os.environ

import os
import database_handler as db_handler
import api_interaction as api
from space_trader_classes import *

print("Hello World!")

if __name__ == "__main__":
    #Just a test to see if the SpaceTraderAPI class works correctly.
    agent = db_handler.get_agent("TEST")
    api.get_all_system(agent_token=agent.agent_token, db_insert=True)
