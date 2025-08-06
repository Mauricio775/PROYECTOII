from typing import Optional

def get_inventory_filter_query(filtro: Optional[str] = None) -> dict:
    query = {}
    if filtro:
        query["description"] = {"$regex": filtro, "$options": "i"}
    return query
