from tools.serper_search import _serper_search
from langchain_core.tools import tool

@tool
def search_energy_sources(query:str)-> str:
    """Search for India energy-security and fuel-import information via
    Serper. Only accepts queries about crude oil, petroleum imports,
    ethanol blending, or energy security — rejects food/water or
    vehicle queries."""
    allowed = ["crude oil", "import", "petroleum", "ethanol blend", "E20", "energy security"]
    if not any(k.lower() in query.lower() for k in allowed):
        return "Query rejected: outside energy-security scope for this tool."
    try:
        return str(_serper_search(query))
    except Exception:
        return "Search unavailable — energy-security scope only." 

@tool
def search_food_water_sources(query: str) -> str:
    """Search for India food-security, agriculture, and water-resource
    information via Serper. Only accepts queries about maize, sugarcane,
    rice, pulses, farmland, or groundwater — rejects energy or vehicle
    queries."""
    allowed = ["maize", "sugarcane", "rice", "pulses", "groundwater", "farmland", "crop"]
    if not any(k.lower() in query.lower() for k in allowed):
        return "Query rejected: outside food/water scope for this tool."
    try:
        return str(_serper_search (query))
    except Exception:
        return "Search unavailable — food/water scope only."

@tool
def search_vehicle_sources(query: str) -> str:
    """Search for India vehicle-compatibility and mileage information via
    Serper. Only accepts queries about mileage, engines, or vehicle
    compatibility — rejects energy or food/water queries."""
    allowed = ["mileage", "engine", "compatibility", "vehicle class", "E20", "fuel economy"]
    if not any(k.lower() in query.lower() for k in allowed):
        return "Query rejected: outside vehicle/consumer scope for this tool."
    try:
        return str(_serper_search(query))
    except Exception:
        return "Search unavailable — vehicle/consumer scope only."