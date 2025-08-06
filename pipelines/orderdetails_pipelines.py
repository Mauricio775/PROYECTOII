from utils.mongodb import get_collection

order_details_collection = get_collection("orderdetails")

def get_order_details_grouped_pipeline() -> list:
    return [
        {
            "$group": { # Agrupar los documentos de la colección orderdetails por orden (id_order)
                "_id": "$id_order",
                "total_items": { "$sum": "$quantity" },
                "unique_books": { "$addToSet": "$id_inventory" }, #$addToSet agrega elementos a un arreglo sin duplicados. Es como un SET en matemáticas: si ya existe, no lo agrega otra vez.


                "lines": { "$sum": 1 }
            }
        },
        {
            "$project": { # Es para proyectar los campos 
                "id_order": "$_id", #Renombramos 
                "_id": 0,
                "total_items": 1,
                "unique_books": 1,
                "lines": 1
            }
        }
    ]
