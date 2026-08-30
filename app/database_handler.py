
import sqlalchemy as sa
from dotenv import load_dotenv
import os  
import json

load_dotenv()  # Load environment variables from .env file

class DatabaseHandler: 
    engine = None

    def __init__(self):
        engine_url = "postgresql://{user}:{password}@{host}:{port}/{database}".format(
            user="spacetrader",
            password=os.getenv("DB_PASSWORD"),
            host="localhost",
            port=5432,
            database="spacetrader"
        )
        self.engine = sa.create_engine(engine_url)

    def insert_agent(self, agent_name, token, faction, json_data):
        """
        Inserts a new agent into the database.
        
        :param agent_name: The name of the agent.
        :param token: The token associated with the agent.
        :param faction: The faction of the agent.
        :param json_data: The JSON data associated with the agent.
        """

        connection = self.engine.connect()

        insert_query = sa.text("""
            INSERT INTO agent (agent_name, token, faction, json_data) 
            VALUES (:agent_name, :token, :faction, :json_data)
        """)
        
        connection.execute(insert_query, {"agent_name": agent_name, "token": token, "faction": faction, "json_data": json.dumps(json_data)})
        connection.commit()
        print("Successfully inserted agent into the database.")
        connection.close()