"""
The Programm to write an read in the Database. 
It is based on the Objects from the SpacetradersAPI.
"""
import sqlalchemy as sa
from dotenv import load_dotenv
import os
import json
import api_interaction as api
from space_trader_classes import *
import datetime as dt
load_dotenv()  # Load environment variables from .env file

engine = None  # Declare engine as a global variable

USER="spacetrader"
PASSWORD=os.getenv("DB_PASSWORD")
HOST="localhost"
PORT=5432
DATABASE="spacetrader"

engine_url = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
engine = sa.create_engine(engine_url)

def insert_spacereset(spacereset: SpaceReset):
    """
    Inserts a new space reset into the database.
    
    :param start_time: The time when the space reset started.
    :param end_time: The time when the space reset ended.
    :param api_version: The API version associated with the space reset.
    """
    try:
        current = current_reset()
        if current is not None:
            current_started: dt.datetime = current.started_at
            current_started = current_started.strftime("%Y-%m-%d")
            if current_started == spacereset.started_at:
                print("Der Reset existiert bereits")
                return current

        connection = engine.connect()
        insert_query = sa.text("""
            INSERT INTO spacereset (started_at, ended_at, api_version) 
            VALUES (:start_time, :end_time, :api_version)
        """)

        connection.execute(insert_query, {
            "start_time": spacereset.started_at,
            "end_time": spacereset.ended_at,
            "api_version": spacereset.api_version
        })
        connection.commit()
        print("Successfully inserted space reset into the database.")
        connection.close()
        return current_reset()
    except Exception as e:
        if connection:
            connection.close()

        print(f"Error inserting space reset into the database: {e}")

def current_reset() -> SpaceReset:
    """
    Retrieves the current space reset from the database.
    
    :return:A dictionary containing the current space reset data, 
            or None if no current reset is found.
    """
    try:
        connection = engine.connect()
        select_query = sa.text("""
            SELECT * FROM spacereset 
            WHERE ended_at > now() OR ended_at IS NULL 
            ORDER BY started_at DESC 
            LIMIT 1
        """)

        result = connection.execute(select_query).fetchone()
        connection.close()
        if result:
            result = result._mapping
            return SpaceReset(
                result['reset_id'],
                result['started_at'],
                result['ended_at'],
                result['api_version']
            )  # Convert Row object to dictionary
        else:
            return None
    except Exception as e:
        if connection:
            connection.close()
        print(f"Error retrieving current space reset from the database: {e}")
        return None


def insert_agent(agent: Agent):
    """
    Inserts a new agent into the database.
    
    :param agent_name: The name of the agent.
    :param token: The token associated with the agent.
    :param faction: The faction of the agent.
    :param json_data: The JSON data associated with the agent.
    """

    if agent.reset_id is None:
        agent.reset_id = current_reset().reset_id
    if agent.hq_waypoint is not None and get_waypoint(agent.hq_waypoint) is None:
        api.get_waypoint(agent.hq_waypoint)

    connection = engine.connect()
    try:
        insert_query = sa.text("""
            INSERT INTO agent (reset_id, symbol, agent_token, starting_faction_symbol, hq_waypoint) 
            VALUES (:reset_id, :symbol, :agent_token, :starting_faction, :hq_waypoint)
        """)

        connection.execute(insert_query, {
            "reset_id": agent.reset_id,
            "symbol": agent.symbol,
            "agent_token": agent.agent_token,
            "starting_faction": agent.starting_faction,
            "hq_waypoint": agent.hq_waypoint 
        })
        connection.commit()
        print("Successfully inserted agent into the database.")
        connection.close()
    except Exception as e:
        if connection:
            connection.close()
        print(f"Error inserting agent into the database: {e}")

def get_agent(symbol, reset_id=current_reset().reset_id) -> Agent:
    try:
        connection = engine.connect()
        select_query = sa.text("""
            SELECT * FROM agent WHERE symbol = :symbol AND reset_id = :reset_id LIMIT 1
        """)

        result = connection.execute(
            select_query,
            {"symbol": symbol,
            "reset_id": reset_id}
        ).fetchone()
        connection.close()
        if result is None:
            return None
        result = result._mapping
        result = Agent(
            reset_id=reset_id,
            symbol=symbol,
            agent_token=result["agent_token"],
            starting_faction=result["starting_faction_symbol"],
            hq_waypoint=result["hq_waypoint"]
        )
        return result
    except Exception as e:
        if connection:
            connection.close()
        print(f"Error checking if waypoint exists in the database: {e}")
        return False


def insert_faction(faction: Faction):
    """
    Inserts a new faction into the database.
    
    :param faction: The faction object, which stores the data.
    """

    try:
        insert_query = sa.text("""
            INSERT INTO faction (reset_id, symbol, name, description, hq_waypoint, isRecruiting) 
            VALUES (:reset_id, :symbol, :name, :description, :hq_waypoint, :isRecruiting)
        """)

        if faction.hq_waypoint is not None and get_system(faction.hq_waypoint) is None:
            res = api.get_system(faction.hq_waypoint, os.getenv("SPACETRADER_ACCOUNT_KEY"))

        connection = engine.connect()
        connection.execute(insert_query, {
            "reset_id": faction.reset_id,
            "symbol": faction.symbol,
            "name": faction.name,
            "description": faction.description,
            "hq_waypoint": faction.hq_waypoint,
            "isRecruiting": faction.is_recruiting
        })
        connection.commit()
        print("Successfully inserted faction into the database.")
        connection.close()
    except Exception as e:
        if connection:
            connection.close()
        print(f"Error inserting faction into the database: {e}")

def insert_waypoint(waypoint: Waypoint):
    """
    Inserts a new waypoint into the database.
    
    :param symbol: The symbol of the waypoint.
    """
    if get_waypoint(waypoint.symbol) is not None:
        print("Waypoint already exists in database")
        return

    try:
        if waypoint.system_symbol is not None and get_system(waypoint.system_symbol) is None:
            api.get_system(waypoint.system_symbol)

        connection = engine.connect()

        insert_query = sa.text("""
            INSERT INTO waypoint (reset_id, symbol, system_symbol, type, x, y) 
            VALUES (:reset_id, :symbol, :system_symbol, :type, :x, :y)
        """)

        connection.execute(insert_query, {
            "reset_id": waypoint.reset_id,
            "symbol": waypoint.symbol,
            "system_symbol": waypoint.system_symbol,
            "type": waypoint.type,
            "x": waypoint.x,
            "y": waypoint.y
        })
        connection.commit()
        print("Successfully inserted waypoint into the database.")
        connection.close()


    except Exception as e:
        if connection:
            connection.close()
        print(f"Error inserting waypoint into the database: {e}")

def get_waypoint(symbol):
    """
    Checks if a waypoint with the given symbol exists in the database.
    
    :param symbol: The symbol of the waypoint to check.
    :return: True if the waypoint exists, False otherwise.
    """
    try:
        reset_id = current_reset().reset_id
        connection = engine.connect()
        select_query = sa.text("""
            SELECT * FROM waypoint WHERE symbol = :symbol AND reset_id = :reset_id LIMIT 1
        """)

        result = connection.execute(select_query, {"symbol": symbol,
                                                   "reset_id": reset_id}).fetchone()
        connection.close()
        if result is None:
            return None
        result = result._mapping
        result = Waypoint(result['reset_id'], result['symbol'], result['system_symbol'],
                          result['type'], result['x'], result['y'], None)
        return result
    except Exception as e:
        if connection:
            connection.close()
        print(f"Error checking if waypoint exists in the database: {e}")
        return None

def insert_system(system_obj: System):
    """This function is used to insert a System into the database

    Args:
        system_obj (System): System, which should be inserted
    """
    if get_system(system_obj.symbol) is not None:
        print("System already exists in db")
        return
    try:
        connection = engine.connect()

        insert_query = sa.text("""
            INSERT INTO system (reset_id, symbol, sector_symbol, type, x, y) 
            VALUES (:reset_id, :symbol, :sector_symbol, :type, :x, :y)
        """)
        connection.execute(insert_query, {
            "reset_id": current_reset().reset_id,
            "symbol": system_obj.symbol,
            "sector_symbol": system_obj.sector_symbol,
            "type": system_obj.type,
            "x": system_obj.x,
            "y": system_obj.y
        })

        connection.commit()
        print("Successfully inserted system into the database.")
        connection.close()

    except Exception as e:
        if connection:
            connection.close()
        print(f"Error inserting waypoint into the database: {e}")

def get_system(symbol):
    """
    Checks if a waypoint with the given symbol exists in the database.
    
    :param symbol: The symbol of the waypoint to check.
    :return: the System, None if it does not exits.
    """
    try:
        reset_id = current_reset().reset_id
        connection = engine.connect()
        select_query = sa.text("""
            SELECT * FROM system WHERE symbol = :symbol AND reset_id = :reset_id LIMIT 1
        """)

        result = connection.execute(
            select_query,
            {"symbol": symbol,
            "reset_id": reset_id}
        ).fetchone()
        if result is None:
            connection.close()
            return None
        result = result._mapping
        connection.close()
        result = System(
            result['reset_id'],
            result['symbol'],
            result['sector_symbol'],
            result['type'],
            result['x'],
            result['y']
        )
        return result
    except Exception as e:
        if connection:
            connection.close()
        print(f"Error checking if system exists in the database: {e}")
        return None
