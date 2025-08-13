

def get_inventory_with_book_pipeline() -> list:
  
    return [
        {
            "$lookup": {
                "from": "book",  
                "let": { "invBook": "$id_book" },
                "pipeline": [
                    {
                        "$match": {
                            "$expr": {
                                "$or": [
                                    { "$eq": [ { "$toString": "$_id" }, "$$invBook" ] },  
                                    { "$eq": [ "$_id", "$$invBook" ] }                     
                                ]
                            }
                        }
                    },
                    { "$project": { "_id": 0, "description": 1, "active": 1 } }
                ],
                "as": "book_data"
            }
        },
        { "$unwind": { "path": "$book_data", "preserveNullAndEmptyArrays": True } },
        { "$addFields": { "book_description": "$book_data.description" } },
        {
            "$project": {
                "_id": 1,
                "id_book": 1,
                "name": 1,
                "description": 1,
                "cost": 1,
                "discount": 1,
                "active": 1,
                "book_description": 1
            }
        }
    ]
