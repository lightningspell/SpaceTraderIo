import requests

class SpaceTraderAPI:
    def save_agent_to_db(self, agent_name: str, token: str, faction: str, json_data: dict):
            """
            Saves the agent information to the database.

            :param db_handler: An instance of DatabaseHandler.
            :param agent_name: The name of the agent.
            :param token: The token associated with the agent.
            :param faction: The faction of the agent.
            :param json_data: The JSON data associated with the agent.
            """
            from database_handler import DatabaseHandler
            db_handler = DatabaseHandler()
            
            db_handler.insert_agent(agent_name, token, faction, json_data)

    def api_create_agent(self, account_token: str, agent_name: str, faction: str = "Cosmic") -> dict:
        """_summary_

        Args:
            account_token (str): the account token used for authorization with the SpaceTrader API.
            agent_name (str): The name of the agent to be created.
            faction (str, optional): The factio of the agent. Defaults to "Cosmic".


        Returns:
            dict: The Json response from the SpaceTraders API.
        """
        params = {
            "faction": faction,
            "symbol": agent_name
        }
        headers = {
            "Authorization": f"Bearer {account_token}"
        }
        response = requests.post("https://api.spacetraders.io/v2/register", json=params, headers=headers)
        print(response.status_code)
        if(response.status_code == 201):
            self.save_agent_to_db(agent_name, response.json()['data']['token'], faction, response.json())
        return response.json()

    
    

        
    