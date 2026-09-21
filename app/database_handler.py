
import sqlalchemy as sa
from dotenv import load_dotenv
import os  
import json
import api_interaction as api
from spaceTraderClasses import *
load_dotenv()  # Load environment variables from .env file


engine = None  # Declare engine as a global variable

engine_url = "postgresql://{user}:{password}@{host}:{port}/{database}".format(
    user="spacetrader",
    password=os.getenv("DB_PASSWORD"),
    host="localhost",
    port=5432,
    database="spacetrader"
)
engine = sa.create_engine(engine_url)

def insert_agent(agent_name, token, faction, json_data):
    """
    Inserts a new agent into the database.
    
    :param agent_name: The name of the agent.
    :param token: The token associated with the agent.
    :param faction: The faction of the agent.
    :param json_data: The JSON data associated with the agent.
    """
    try:
        connection = engine.connect()

        insert_query = sa.text("""
            INSERT INTO agent (agent_name, token, faction, json_data) 
            VALUES (:agent_name, :token, :faction, :json_data)
        """)
        
        connection.execute(insert_query, {"agent_name": agent_name, "token": token, "faction": faction, "json_data": json.dumps(json_data)})
        connection.commit()
        print("Successfully inserted agent into the database.")
        connection.close()
    except Exception as e:
        if connection:
            connection.close()
        print(f"Error inserting agent into the database: {e}")


def insert_spacereset(start_time, end_time, api_version = None):
    """
    Inserts a new space reset into the database.
    
    :param start_time: The time when the space reset started.
    :param end_time: The time when the space reset ended.
    :param api_version: The API version associated with the space reset.
    """
    try: 
        connection = engine.connect()
        if api_version is None:
            insert_query = sa.text("""
                INSERT INTO spacereset (started_at, ended_at) 
                VALUES (:start_time, :end_time)
            """)
            
            connection.execute(insert_query, {"start_time": start_time, "end_time": end_time})
        else:
            insert_query = sa.text("""
                INSERT INTO spacereset (started_at, ended_at, api_version) 
                VALUES (:start_time, :end_time, :api_version)
            """)
            
            connection.execute(insert_query, {"start_time": start_time, "end_time": end_time, "api_version": api_version})
        connection.commit()
        print("Successfully inserted space reset into the database.")
        connection.close()
    except Exception as e:
        if connection:
            connection.close()
        print(f"Error inserting space reset into the database: {e}")

def current_reset():
    """
    Retrieves the current space reset from the database.
    
    :return: A dictionary containing the current space reset data, or None if no current reset is found.
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
            return dict(result._mapping)  # Convert Row object to dictionary
        else:
            return None
    except Exception as e:
        if connection:
            connection.close()
        print(f"Error retrieving current space reset from the database: {e}")
        return None

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

        if faction.hq_waypoint is not None and system_exists(faction.hq_waypoint) == False:
            res = api.get_system(faction.hq_waypoint, os.getenv("SPACETRADER_ACCOUNT_KEY"))
            insert_system(res)

        connection = engine.connect()    
        connection.execute(insert_query, {
            "reset_id": faction.reset_id,
            "symbol": faction.symbol,
            "name": faction.name,
            "description": faction.description,
            "hq_waypoint": faction.hq_waypoint,
            "isRecruiting": faction.isRecruiting
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
    
    try:
        connection = engine.connect()

        insert_query = sa.text("""
            INSERT INTO waypoint (reset_id, symbol, system_symbol, type, x, y, orbitals, faction_symbol, traits) 
            VALUES (:reset_id, :symbol, :system_symbol, :type, :x, :y, :orbitals, :faction_symbol, :traits)
        """)
        
        connection.execute(insert_query, {
            "reset_id": waypoint.reset_id,
            "symbol": waypoint.symbol,
            "system_symbol": waypoint.system_symbol,
            "type": waypoint.type,
            "x": waypoint.x,
            "y": waypoint.y,
            "orbits_waypoint": waypoint.orbits_waypoint
        })
        connection.commit()
        print("Successfully inserted waypoint into the database.")
        connection.close()
    except Exception as e:
        if connection:
            connection.close()
        print(f"Error inserting waypoint into the database: {e}")

def waypoint_exists(symbol):
    """
    Checks if a waypoint with the given symbol exists in the database.
    
    :param symbol: The symbol of the waypoint to check.
    :return: True if the waypoint exists, False otherwise.
    """
    try:
        reset_id = current_reset()['reset_id']
        connection = engine.connect()
        select_query = sa.text("""
            SELECT 1 FROM waypoint WHERE symbol = :symbol AND reset_id = :reset_id LIMIT 1
        """)
        
        result = connection.execute(select_query, {"symbol": symbol, "reset_id": reset_id}).fetchone()
        connection.close()
        return result is not None
    except Exception as e:
        if connection:
            connection.close()
        print(f"Error checking if waypoint exists in the database: {e}")
        return False

def insert_system(systemObj: System):
    try:
        connection = engine.connect()

        insert_query = sa.text("""
            INSERT INTO system (reset_id, symbol, sector_symbol, type, x, y) 
            VALUES (:reset_id, :symbol, :sector_symbol, :type, :x, :y)
        """)
        
        connection.execute(insert_query, {
            "reset_id": current_reset()['reset_id'],
            "symbol": systemObj.symbol,
            "sector_symbol": systemObj.sectorSymbol,
            "type": systemObj.type,
            "x": systemObj.x,
            "y": systemObj.y
        })

        connection.commit()
        print("Successfully inserted system into the database.")
        connection.close()

    except Exception as e:
        if connection:
            connection.close()
        print(f"Error inserting waypoint into the database: {e}")

def system_exists(symbol):
    """
    Checks if a waypoint with the given symbol exists in the database.
    
    :param symbol: The symbol of the waypoint to check.
    :return: True if the waypoint exists, False otherwise.
    """
    try:
        reset_id = current_reset()['reset_id']
        connection = engine.connect()
        select_query = sa.text("""
            SELECT 1 FROM system WHERE symbol = :symbol AND reset_id = :reset_id LIMIT 1
        """)
        
        result = connection.execute(select_query, {"symbol": symbol, "reset_id": reset_id}).fetchone()
        connection.close()
        return result is not None
    except Exception as e:
        if connection:
            connection.close()
        print(f"Error checking if system exists in the database: {e}")
        return False