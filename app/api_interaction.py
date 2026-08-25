import requests

class SpaceTraderAPI:
    def api_create_agent(self, account_token: str, agent_name: str, faction: str = "Cosmic") -> dict:
        params = {
            "faction": faction,
            "symbol": agent_name
        }
        headers = {
            "Authorization": f"Bearer {account_token}"
        }
        response = requests.post("https://api.spacetraders.io/v2/register", json=params, headers=headers)
        print(response.status_code)
        return response.json()

        
    