"""
This module is used to interact with the api.
"""

import os

import database_handler as db_handler
from api_client import ApiError, api_request
from dotenv import load_dotenv
from space_trader_classes import Agent, Faction, SpaceReset, System, Waypoint

load_dotenv()

def create_agent(agent_name: str,
                 account_token: str = os.getenv("SPACETRADER_ACCOUNT_KEY"),
                 faction: str = "COSMIC",
                 db_insert: bool = False) -> Agent:
    """_summary_

    Args:
        account_token (str): the account token used for authorization with the SpaceTrader API.
        agent_name (str): The name of the agent to be created.
        faction (str, optional): The factio of the agent. Defaults to "Cosmic".
        db_insert (bool, optional): If true the agent is saved in the DB. Defaults to False

    Returns:
        dict: The Json response from the SpaceTraders API.
    """
    params = {
        "symbol": agent_name,
        "faction": faction
    }
    try:
        body = api_request(
            "Post",
            "/register",
            account_token,
            json=params
        )
        data = body["data"]
    except ApiError as e:
        print(f"API-FEHLER: {e.status_code}: {e.body}")
        return None

    agent = Agent(db_handler.current_reset().reset_id, data['agent']['symbol'],
                data['token'], data['faction']['symbol'], data['agent']['headquarters'])
    if db_insert:
        agent.insert_into_db()
    return agent

def api_get_reset_info(db_insert: bool = False) -> SpaceReset:
    """This function gets the informations of the current reset

    Args:
        db_insert (bool, optional): If true the reset is saved to the database. Defaults to False.

    Returns:
        SpaceReset: Returns the current Reset of the Spacetrader API
    """
    try:
        response = api_request("Get", "")
    except ApiError as e:
        print(f"API-FEHLER: {e.status_code}: {e.body}")
        return None
    started_at = response['resetDate']
    ended_at = response['serverResets']['next']
    version = response['version']

    reset = SpaceReset(None, started_at, ended_at, version)

    if db_insert:
        reset = reset.insert_into_db()

    return reset

def get_all_factions(account_token: str = os.getenv("SPACETRADER_ACCOUNT_KEY"), db_insert: bool = False) -> list:
    """Retrieves all factions from the Spacetrader API, as a list

    Args:
        account_token (str, optional): The token of the spacetraderAPI account, which is used and stored in the .env. Defaults to os.getenv("SPACETRADER_ACCOUNT_KEY").
        db_insert (bool, optional): if true safes all missing factions to the database. Defaults to False.

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
            if db_insert:
                db_handler.insert_faction(fact)
            
            res.append(fact)
        return res
    except Exception as e:
        print(f"Error retrieving factions from the SpaceTraders API: {e}")

def get_waypoint(waypoint_symbol: str,
                 agent_token: str = os.getenv("SPACETRADER_ACCOUNT_KEY"),
                 db_insert: bool = False) -> Waypoint:
    """This function retrieves all data regarding a waypoint from the spacetrader API.

    Args:
        waypoint_symbol (str): The symbol of the waypoint to retrieve.
        agent_token (str): The agent token used for authorization with the SpaceTrader API.
        db_insert (bool): If true the waypoint is safed to the db. Defaults to False
    Returns:
        dict: The Json response from the SpaceTraders API.
    """
    parts = waypoint_symbol.split("-")
    system_symbol = "-".join(parts[:2])

    try:
        response = api_request("Get", f"/systems/{system_symbol}/waypoints/{waypoint_symbol}", agent_token)
    except ApiError as e:
        print(f"API-FEHLER: {e.status_code}: {e.body}")
        return

    data = response['data']
    way = Waypoint(db_handler.current_reset().reset_id, data['symbol'], data['systemSymbol'],
                   data['type'], data['x'], data['y'], str(data['orbitals']))
    if db_insert:
        way.insert_into_db()
    return way

def get_system(system_symbol: str, agent_token :str, db_insert: bool = False) -> System:
    """Retrieves a certain system by its symbol in the Spacetrader API

    Args:
        system_symbol (str): the symbol of the System
        agent_token (str): the token of the agent, which is used to retrieve the Data
        db_insert (bool, optional): if true the system is saved in the db. Defaults to False.

    Returns:
        System: Retrurns the System from the API.
    """
    try:
        response = api_request("Get", f"/systems/{system_symbol}", agent_token)
    except ApiError as e:
        print(f"API-FEHLER: {e.status_code}: {e.body}")
        return

    data = response['data']
    system = System(db_handler.current_reset().reset_id, data['symbol'], data['sectorSymbol'],
                    data['type'], data['x'], data['y'])
    if db_insert:
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
        systems.append(system)
        system.insert_into_db()
        if db_insert:
            get_all_waypoints_in_system(system.symbol, agent_token, True, reset_id.reset_id)


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

            system.insert_into_db()
            systems.append(system)
            if db_insert:
                get_all_waypoints_in_system(system.symbol, agent_token, True, reset_id.reset_id)


            systems.append(system)
    return systems

def get_all_waypoints_in_system(system_symbol: str, agent_token : str, db_insert : bool, reset_id : int):
    try:
        ways = []
        body = api_request(
            "Get",
            f"/systems/{system_symbol}/waypoints",
            agent_token
        )
        for waypoint in body["data"]:
            way = Waypoint(reset_id, waypoint["symbol"], system_symbol,
                            waypoint["type"], waypoint["x"], waypoint["y"], waypoint["orbitals"])
            way.insert_into_db()
            for orbital in waypoint["orbitals"]:
                db_handler.insert_orbital(waypoint["symbol"],
                                        orbital["symbol"], reset_id)
            for trait in waypoint["traits"]:
                if db_handler.check_waypoint_trait(trait["symbol"]) is False:
                    db_handler.insert_waypoint_trait(trait["symbol"], trait["name"], trait["description"])
                db_handler.insert_waypoint_trait_link(way.symbol, trait["symbol"], reset_id)
            for modifier in waypoint["modifiers"]:
                if db_handler.check_waypoint_trait(modifier["symbol"]) is False:
                    db_handler.insert_waypoint_trait(modifier["symbol"], modifier["name"], modifier["description"])
                db_handler.insert_waypoint_trait_link(way.symbol, modifier["symbol"], reset_id)
            ways.append(way)
        return ways

    except ApiError as e:
        print(f"API Fehler: {e.status_code} : {e.body}")
        return None
    except Exception as e:
        print(f"Error Getting and Inserting Waypoints in Database: {e}")
        return None
