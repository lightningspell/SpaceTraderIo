from dotenv import load_dotenv
import os
import requests

load_dotenv()

account_token = os.getenv("SPACETRADER_ACCOUNT_KEY")
res = requests.get("https://api.spacetraders.io/v2/agents",
    headers={
      "Authorization": f"Bearer {account_token}"
    }
)
print(res.json()['data'])