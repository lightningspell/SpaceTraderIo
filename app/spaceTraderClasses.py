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