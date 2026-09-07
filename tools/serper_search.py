import os
import requests
from dotenv import load_dotenv

load_dotenv(override=True)

def _serper_search(query: str):
    resp = requests.post(
        "https://google.serper.dev/search",
        headers={"X-API-KEY": os.environ["SERPER_API_KEY"]},
        json={"q": query},
        timeout=10
    )
    resp.raise_for_status()
    return resp.json()