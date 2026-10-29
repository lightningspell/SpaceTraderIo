"""
The main script: it is used to conncet all other modules to achive a complete programm. 
"""

import api_interaction as api
import database_handler as db_handler
from dotenv import load_dotenv
import reset_handler

load_dotenv()  # reds .env

print("Hello World!")

if __name__ == "__main__":
    #Just a test to see if the SpaceTraderAPI class works correctly.
    reset_handler.sync_universe()
