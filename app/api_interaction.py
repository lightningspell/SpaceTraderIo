import os
import requests
import database_handler as db_handler
from space_trader_classes import *
from dotenv import load_dotenv
from api_client import api_request, ApiError

load_dotenv()

def create_agent(agent_name: str,
                 account_token: str = os.getenv("SPACETRADER_ACCOUNT_KEY"),
                 faction: str = "COSMIC") -> Agent:
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
    try:
        data = api_request(
            "Post",
            "/register",
            account_token,
            params=params
        )["data"]
    except ApiError as e:
        print(f"API-FEHLER: {e.status_code}: {e.body}")
        return None

    agent = Agent(db_handler.current_reset().reset_id, data['agent']['symbol'],
                data['token'], data['faction']['symbol'], data['agent']['headquarters'])
    agent.insert_into_db()
    return agent

def get_agent(account_token: str = os.getenv("SPACETRADER_ACCOUNT_KEY")):
    """_summary_

    Args:
        account_token (str): the account token used for authorization with the SpaceTrader API.

    Returns:
        dict: The Json response from the SpaceTraders API.
    """
    try:
        data = api_request(
            "Get",
            "/my/agent",
            account_token
        )["data"]
    except ApiError as e:
        print(f"API-FEHLER: {e.status_code}: {e.body}")
        return   
    print(data)

def api_get_reset_info() -> SpaceReset:
    """_summary_

    Returns:
        dict: The Json response from the SpaceTraders API.
    """
    try:
        response = api_request("Get", "")
    except ApiError as e:
        print(f"API-FEHLER: {e.status_code}: {e.body}")
        return None 
   
    started_at = response.json()['resetDate']
    ended_at = response.json()['serverResets']['next']
    version = response.json()['version']

    reset = SpaceReset(None, started_at, ended_at, version)

    reset = reset.insert_into_db()

    return reset



def get_all_factions(account_token: str = os.getenv("SPACETRADER_ACCOUNT_KEY")) -> list:
    """_summary_

    Returns:
        list: A list of all factions available in the SpaceTraders API.
    """
    try:
        response = api_request("Get", "/factions", account_token)
    except ApiError as e:
        print(f"API-FEHLER: {e.status_code}: {e.body}")
        return   
    
    res = []
    try:
        for faction in response['data']:
            fact = Faction(db_handler.current_reset().reset_id, faction['symbol'], faction['name'],
                           faction['description'], faction['headquarters'], faction['isRecruiting'])
            db_handler.insert_faction(fact)
            res.append(fact)
        return res
    except Exception as e:
        print(f"Error retrieving factions from the SpaceTraders API: {e}")

def get_waypoint(waypointSymbol: str,
                 account_token: str = os.getenv("SPACETRADER_ACCOUNT_KEY")) -> Waypoint:
    """_summary_

    Args:
        symbol (str): The symbol of the waypoint to retrieve.
        account_token (str): The account token used for authorization with the SpaceTrader API.

    Returns:
        dict: The Json response from the SpaceTraders API.
    """
    parts = waypointSymbol.split("-")
    system_symbol = "-".join(parts[:2])

    try:
        response = api_request("Get", f"/systems/{system_symbol}/waypoints/{waypointSymbol}", account_token)
    except ApiError as e:
        print(f"API-FEHLER: {e.status_code}: {e.body}")
        return
       
    data = response['data']
    way = Waypoint(db_handler.current_reset().reset_id, data['symbol'], data['systemSymbol'],
                   data['type'], data['x'], data['y'], str(data['orbitals']))
    way.insert_into_db()
    return way

def get_system(system_symbol: str, account_token = os.getenv("SPACETRADER_ACCOUNT_KEY")) -> System:
    """_summary_

    Args:
        system_symbol (_type_): _description_
    """
    try:
        response = api_request("Get", f"/systems/{system_symbol}", account_token)
    except ApiError as e:
        print(f"API-FEHLER: {e.status_code}: {e.body}")
        return

    data = response['data']
    system = System(db_handler.current_reset().reset_id, data['symbol'], data['sectorSymbol'],
                    data['type'], data['x'], data['y'])
    system.insert_into_db()
    return system

def get_all_system(agent_token = os.getenv("SPACETRADER_ACCOUNT_KEY"), db_insert=False) -> list[System]:
    """This function is used to get all systems in the current reset, it returns a list of all Systems.

    Args:
        account_token (_type_, optional): _description_. Defaults to os.getenv("SPACETRADER_ACCOUNT_KEY"), 
        db_insert (bool, optional): If set to true the function will save all Systems and Waypoints to the db. Defaults to false

    Returns:
        list(Systems): The functions returns a list of all Systems in the current reset. 
    """
    systems = []

    reset_id = db_handler.current_reset()
    try:
        body = api_request(
            "Get", 
            "/systems", 
            token=agent_token,
            params={
                "page":"1",
                "limit": "20"
            }
        )
    except ApiError as e:
        print(f"API-FEHLER: {e.status_code}: {e.body}")
        return

    meta = body["meta"]
    max_pages = int(meta["total"]) // 20 + 1

    data = body['data']

    for row in data:
        system = System(reset_id.reset_id, row['symbol'], row['sectorSymbol'],
                        row['type'], row['x'], row['y'])

        if db_insert:
            system.insert_into_db()
            for waypoint in row["waypoints"]:
                way = Waypoint(reset_id.reset_id, waypoint["symbol"], row["symbol"],
                               waypoint["type"], waypoint["x"], waypoint["y"], waypoint["orbitals"])
                way.insert_into_db()

        systems.append(system)

    for page in range(1,max_pages):
        try:
            body = api_request(
                "Get", 
                "/systems", 
                token=agent_token, 
                params={
                    "page":f"{page}",
                    "limit": "20"
                }
            )
        except ApiError as e:
            print(f"API-FEHLER: {e.status_code}: {e.body}")
            return

        data = body['data']
        for row in data:
            system = System(reset_id, row['symbol'], row['sectorSymbol'],
                            row['type'], row['x'], row['y'])

            if db_insert:
                for waypoint in row["waypoints"]:
                    way = Waypoint(reset_id.reset_id, waypoint["symbol"], row["symbol"],
                                   waypoint["type"], waypoint["x"], waypoint["y"], waypoint["orbitals"])
                    way.insert_into_db()
                system.insert_into_db()
            systems.append(system)
    return systems
