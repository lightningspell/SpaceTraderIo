"""
This module is used to implement Datastruktures, 
which represent a number of Objects inside the SpacetradersAPI.
"""

import database_handler as db_handler


class System:
    """
    Represents a System in the SpacetraderAPI
    """
    def __init__(self, reset_id: int, system_symbol:str, sector_symbol:str, type: str, x: int, y: int):
        self.symbol = system_symbol
        self.reset_id = reset_id
        self.sector_symbol = sector_symbol
        self.type = type
        self.x = x
        self.y = y


    def insert_into_db(self):
        """
        This functions adds this Object to the Database in the current Reset.
        """
        db_handler.insert_system(self)

class Waypoint:
    """
    Represents a Waypoint in the SpacetraderAPI
    """
    def __init__(self, reset_id: id, symbol: str, system_symbol: str, type: str, x: int, y: int, orbits_waypoint: str = None):
        self.reset_id = reset_id
        self.symbol = symbol
        self.system_symbol = system_symbol
        self.type = type
        self.x = x
        self.y= y
        self.orbits_waypoint = orbits_waypoint

    def insert_into_db(self):
        """
        Inserst this Waypoint in the Database in the current reset
        """
        db_handler.insert_waypoint(self)

class Faction:
    """
    Represents a Faction in the SpacetraderAPI
    """
    def __init__(self, reset_id: int, symbol: str, name: str, description: str = None, hq_waypoint: str = None, is_recruiting: bool = None):
        self.reset_id = reset_id
        self.symbol = symbol
        self.name = name
        self.description = description
        self.hq_waypoint = hq_waypoint
        self.is_recruiting = is_recruiting

    def insert_into_db(self):
        """
        Inserts this Faction in the Database in the current reset
        """
        db_handler.insert_faction(self)

class SpaceReset:
    """
    Represents a Reset in the SpacetraderAPI
    """
    def __init__(self, reset_id: int, started_at, ended_at, api_version):
        self.reset_id = reset_id
        self.started_at = started_at
        self.ended_at = ended_at
        self.api_version = api_version

    def insert_into_db(self):
        """
        Inserts this Reset in the Database

        Returns:
            SpaceResets: retrurns a new Version of its self, with the correct Id 
        """
        db_handler.insert_spacereset(self)
        reset = db_handler.current_reset()
        if self.reset_id is None and reset is not None:
            self.reset_id = reset.reset_id
            return self

class Agent:
    """
    Represents an Agent in the SpacetraderAPI
    """
    def __init__(self, reset_id: int, symbol, agent_token, starting_faction, hq_waypoint):
        self.reset_id = reset_id
        self.symbol = symbol
        self.agent_token = agent_token
        self.starting_faction = starting_faction
        self.hq_waypoint = hq_waypoint

    def insert_into_db(self):
        """
        Insert this Object into the Database
        """
        db_handler.insert_agent(self)

