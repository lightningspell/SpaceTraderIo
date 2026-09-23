import database_handler as db_handler


class System:
    def __init__(self, reset_id: int, systemSymbol:str, sectorSymbol:str, type: str, x: int, y: int):
        self.symbol = systemSymbol
        self.reset_id = reset_id
        self.sectorSymbol = sectorSymbol
        self.type = type
        self.x = x
        self.y = y

    def insert_into_db(self):
        db_handler.insert_system(self)

class Waypoint:
    def __init__(self, reset_id: id, symbol: str, system_symbol: str, type: str, x: int, y: int, orbits_waypoint: str = None):
        self.reset_id = reset_id
        self.symbol = symbol
        self.system_symbol = system_symbol
        self.type = type
        self.x = x
        self.y= y
        self.orbits_waypoint = orbits_waypoint

    def insert_into_db(self):
        db_handler.insert_waypoint(self)

class Faction:
    def __init__(self, reset_id: id, symbol: str, name: str, description: str = None, hq_waypoint: str = None, isRecruiting: bool = None):
        self.reset_id = reset_id
        self.symbol = symbol
        self.name = name
        self.description = description
        self.hq_waypoint = hq_waypoint
        self.isRecruiting = isRecruiting
        
    
    def insert_into_db(self):
        db_handler.insert_faction(self)

class SpaceReset:
    def __init__(self, reset_id, started_at, ended_at, api_version):
        self.reset_id = reset_id
        self.started_at = started_at
        self.ended_at = ended_at
        self.api_version = api_version

    def insert_into_db(self):
        db_handler.insert_spacereset(self)
        reset = db_handler.current_reset()
        if self.reset_id is None and reset is not None:
            self.reset_id = reset.reset_id
            return self
        # TODO: Sollte man später Resets auch in die Zukunft planen muss man das hier überarbeiten.
class Agent:
    def __init__(self, reset_id, symbol, agent_token, starting_faction, hq_waypoint):
        self.reset_id = reset_id
        self.symbol = symbol
        self.agent_token = agent_token
        self.starting_faction = starting_faction
        self.hq_waypoint = hq_waypoint

    def insert_into_db(self):
        db_handler.insert_agent(self)

