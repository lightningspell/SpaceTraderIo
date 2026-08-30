from dotenv import load_dotenv
load_dotenv()  # liest .env aus dem aktuellen Arbeitsverzeichnis und setzt os.environ

import os

print("Hello World!")

if __name__ == "__main__":
    # Just a test to see if the SpaceTraderAPI class works correctly.
    from api_interaction import SpaceTraderAPI

    api = SpaceTraderAPI()
    agent_name = "test13"
    faction = "COSMIC"  # Replace with your desired faction
    account_token = os.getenv("SPACETRADER_ACCOUNT_KEY")  # Get the account token from environment variable
    print(api.api_create_agent(account_token, agent_name, faction))