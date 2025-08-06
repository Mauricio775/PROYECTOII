from bson import ObjectId

def get_all_payment_history_pipeline():
    return [
        { 
            "$lookup": {  
                "from": "payments", 
                "let": {"payment_id": {"$toObjectId": "$id_payments"}}, 
                "pipeline": [ 
                    {"$match": {"$expr": {"$eq": ["$_id", "$$payment_id"]}}},
                    {"$project": {"_id": 0, "date": 1, "total": 1}}
                ],
                "as": "payment_info" 
            }
        },
        {
            "$lookup": { 
                "from": "states",
                "let": {"state_id": {"$toObjectId": "$id_state"}}, 
                "pipeline": [ 
                    {"$match": {"$expr": {"$eq": ["$_id", "$$state_id"]}}},
                    {"$project": {"_id": 0, "name": 1}}
                ],
                "as": "state_info" 
            }
        },
        {
            "$lookup": { 
                "from": "payments_type", 
                "let": {"type_id": {"$toObjectId": "$id_payments_type"}}, 
                "pipeline": [
                    {"$match": {"$expr": {"$eq": ["$_id", "$$type_id"]}}}, 
                    {"$project": {"_id": 0, "state_method": 1}}
                ],
                "as": "type_info" 
            }
        },
        {
            "$project": {  
                "id": {"$toString": "$_id"}, 
                "quantity": 1,
                "payment_info": {"$arrayElemAt": ["$payment_info", 0]},
                "state_info": {"$arrayElemAt": ["$state_info", 0]},  
                "type_info": {"$arrayElemAt": ["$type_info", 0]},
                "_id": 0
            }
        }
    ]

def get_payment_history_by_id_pipeline(payment_history_id: str):
    return [
        {"$match": {"_id": ObjectId(payment_history_id)}} 
    ] + get_all_payment_history_pipeline()