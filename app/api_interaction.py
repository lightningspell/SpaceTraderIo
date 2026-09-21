from urllib import response

import requests
import database_handler as db_handler
from spaceTraderClasses import *
        
def api_create_agent(account_token: str, agent_name: str, faction: str = "Cosmic") -> dict:
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
        db_handler.insert_agent(agent_name, response.json()['data']['token'], faction, response.json())
    return response.json()

def api_get_reset_info() -> dict:
    """_summary_

    Returns:
        dict: The Json response from the SpaceTraders API.
    """
    response = requests.get("https://api.spacetraders.io/v2")
    print(f"Response status code: {response.status_code}")
    if(response.status_code == 200):
        started_at = response.json()['resetDate']
        ended_at = response.json()['serverResets']['next']
        version = response.json()['version']

        db_handler.insert_spacereset(started_at, ended_at, version) 

        return {'started_at': started_at, 'ended_at': ended_at, 'version': version}



def get_all_factions(account_token: str) -> list:
    """_summary_

    Returns:
        list: A list of all factions available in the SpaceTraders API.
    """
    response = requests.get("https://api.spacetraders.io/v2/factions",
        headers={
        "Authorization": account_token
        }
    )
    res = []
    try: 

        for faction in response.json()['data']:
            fact = Faction(db_handler.current_reset()['reset_id'], faction['symbol'], faction['name'], faction['description'], faction['headquarters'], faction['isRecruiting'])
            db_handler.insert_faction(fact)
            res.append(fact)
        return res
    except Exception as e:
        print(f"Error retrieving factions from the SpaceTraders API: {e}")

def get_waypoint(systemSymbol: str, account_token: str) -> Waypoint:
    """_summary_

    Args:
        symbol (str): The symbol of the waypoint to retrieve.
        account_token (str): The account token used for authorization with the SpaceTrader API.

    Returns:
        dict: The Json response from the SpaceTraders API.
    """
    response = requests.get(f"https://api.spacetraders.io/v2/systems/{systemSymbol}/waypoints/{waypointSymbol}",
        headers={
            "Authorization": account_token
        },
    )
    data = response.json()['data']
    way = Waypoint(db_handler.current_reset()['reset_id'], data['symbol'], data['systemSymbol'], data['type'], data['x'], data['y'], data['orbits_waypoint'])
    return way

def get_system(systemSymbol: str, account_token) -> System:
    """_summary_

    Args:
        systemSymbol (_type_): _description_
    """
    response = requests.get(
        f"https://api.spacetraders.io/v2/systems/{systemSymbol}",
        headers={"Authorization": account_token}
    )
    if response.status_code != 200:
        print(f"Fehler {response.status_code}: {response.json()}")
        return None
    data = response.json()['data']
    system = System(db_handler.current_reset()['reset_id'], data['symbol'], data['sectorSymbol'], data['type'], data['x'], data['y'])
    system.insert_into_db()
    return system


    



    
