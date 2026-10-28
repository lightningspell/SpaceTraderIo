"""
The main script: it is used to conncet all other modules to achive a complete programm. 
"""

import api_interaction as api
import database_handler as db_handler
from dotenv import load_dotenv

load_dotenv()  # reds .env

print("Hello World!")

if __name__ == "__main__":
    #Just a test to see if the SpaceTraderAPI class works correctly.
    agent = db_handler.get_agent("TEST")
    api.get_all_system(agent_token=agent.agent_token, db_insert=True)
