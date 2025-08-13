def get_inventory_with_book_pipeline() -> list:
    

    return [
        # Normaliza a string el id_book del inventario
        {"$addFields": {"id_book_str": {"$toString": "$id_book"}}},

        {
            "$lookup": {
                "from": "book",  
                "let": {"idb": "$id_book_str"},
                "pipeline": [
                    {"$addFields": {"_id_str": {"$toString": "$_id"}}},
                    {"$match": {"$expr": {"$eq": ["$_id_str", "$$idb"]}}},
                    {"$project": {"_id": 0, "description": 1, "active": 1}}
                ],
                "as": "book_data"
            }
        },

        # Saca un único documento o permite nulo si no hay match
        {"$unwind": {"path": "$book_data", "preserveNullAndEmptyArrays": True}},

        # Agrega la descripción del tipo
        {"$addFields": {"book_description": "$book_data.description"}},

        # Limpia campos auxiliares
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

