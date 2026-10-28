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
    - Waypoints & Systems -> Traits are missing 
    - Factions + Traits -> Faction links are still missing

    """
    api.api_get_reset_info()
    technichal_agent = api.create_agent("technical_user")
    if technichal_agent is None:
        technichal_agent = get_agent("technical_user")
    api.get_all_system(agent_token=technichal_agent.agent_token, db_insert=True)
    api.get_all_factions()
