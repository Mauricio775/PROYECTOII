from bson import ObjectId


def  get_book_pipeline() -> list:
    return [
        {
            "$addFields": {
                "id": {"$toString": "$_id"}
            }
        },{
            "$lookup": {
                "from": "inventory",
                "localField": "id",
                "foreignField": "id_book",
                "as": "result"
            }
        },{
            "$group": {
                "_id": {
                    "id": "$id",
                    "description": "$description",
                    "active": "$active"
                },
                "number_of_products": {
                    "$sum": {"$size": "$result"}
                }
            }
        },{
            "$project": {
                "_id": 0,
                "id": "$_id.id",
                "description": "$_id.description",
                "active": "$_id.active",
                "number_of_products": 1
            }
        }
    ]
    
    
    
def validate_book_assigned_pipeline() -> list:
     return [
        {
            "$match": {
                "_id": ObjectId(id),
            }
        },{
            "$addFields": {
                "id": {"$toString": "$_id"}
            }
        },{
            "$lookup": {
                "from": "inventory",
                "localField": "id",
                "foreignField": "id_book",
                "as": "result"
            }
        },{
            "$group": {
                "_id": {
                    "id": "$id",
                    "description": "$description",
                    "active": "$active"
                },
                "number_of_products": {
                    "$sum": {"$size": "$result"}
                }
            }
        },{
            "$project": {
                "_id": 0,
                "id": "$_id.id",
                "description": "$_id.description",
                "active": "$_id.active",
                "number_of_products": 1
            }
        }
    ]