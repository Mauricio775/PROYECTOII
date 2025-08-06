from bson import ObjectId

def get_all_payments_type_pipeline():
    return [
        {
            "$lookup": {
                "from": "payments",
                "let": {"payment_id": {"$toObjectId": "$id_payments"}},
                "pipeline": [
                    {"$match": {"$expr": {"$eq": ["$_id", "$$payment_id"]}}}
                ],
                "as": "payment_info"
            }
        },
        {
            "$project": {
                "id": {"$toString": "$_id"},             
                "id_payments": 1,                         
                "payments_amount": {"$arrayElemAt": ["$payment_info.amount", 0]},  
                "payment_method": {"$arrayElemAt": ["$payment_info.state_method", 0]},  
                "_id": 0
            }
        }
    ]

def get_payment_type_by_id_pipeline(payment_type_id: str):
    return [
        {
            "$match": {
                "_id": ObjectId(payment_type_id)
            }
        }
    ] + get_all_payments_type_pipeline() 
    
    
