"""
The Reset_handler should include all interaction, 
which are necessary at the start or end of a reset.
"""

import api_interaction as api
from database_handler import get_agent


def sync_universe():
    """
    This function is used to sync the universe to the database. 
    It syncs:
    - Reset
    - a technical Agent
    - Waypoints & Systems -> Traits has to be fixed 
    - Factions + Traits -> Faction links are still missing

    """
    reset = api.api_get_reset_info(True)
    technichal_agent = get_agent("tech_a1", reset_id=reset.reset_id)
    if technichal_agent is None:
        technichal_agent = api.create_agent("tech_a1")
        technichal_agent.hq_waypoint = None
        technichal_agent.starting_faction = None
        technichal_agent.insert_into_db()
    api.get_all_system(agent_token=technichal_agent.agent_token, db_insert=True)
    api.get_all_factions()
