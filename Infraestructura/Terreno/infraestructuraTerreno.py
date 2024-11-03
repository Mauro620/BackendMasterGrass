from Dominio.Terreno.modeloTerreno import ModeloTerreno
from bson import ObjectId
import pymongo

#------------------ Terreno ------------------#
class InfraestructuraTerreno:

    def __init__(self) -> None:
        pass
        
    def consultar_terreno_todo(self):
        results = []
        connection_string = "mongodb+srv://mcorreace:sywv6ZiKRwQGwOJi@cluster0.55ale.mongodb.net/MasterGrass?retryWrites=true&w=majority&appName=Cluster0"
        database_name = "MasterGrass"
        collection_name = "Terreno"
        client = pymongo.MongoClient(connection_string)
        try:
            db = client[database_name]
            col = db[collection_name]
            result = col.find()
            
            for item in list(result):
                results.append(ModeloTerreno.terreno_helper(item))
        
        except Exception as ex:
            print(f"Consultar Terreno Todo Fallido: {ex}")
        finally:
            client.close()
        return results

#-------------------------------------------------------------------
    def consultar_terreno_id(self, id:str):
        resultado = []
        connection_string = "mongodb+srv://mcorreace:sywv6ZiKRwQGwOJi@cluster0.55ale.mongodb.net/MasterGrass?retryWrites=true&w=majority&appName=Cluster0"
        database_name = "MasterGrass"
        collection_name = "Terreno"
        client = pymongo.MongoClient(connection_string)
        try:
            db = client[database_name]
            col = db[collection_name]
            result = col.find(
                {
                    "_id": ObjectId(id)
                })
            for item in list(result):
                resultado.append(ModeloTerreno.terreno_helper(item))
            print(f"Consultar Terreno Id Exitoso")
        except Exception as ex:
            resultado = f"Consultar Terreno Id Fallido: {ex}"
        finally:
            client.close()
        return resultado
    

    # --------------------------------------------------------------------------------
    def ingresar_terreno(self, modelo_terreno: ModeloTerreno):
        resultado = []
        connection_string = "mongodb+srv://mcorreace:sywv6ZiKRwQGwOJi@cluster0.55ale.mongodb.net/MasterGrass?retryWrites=true&w=majority&appName=Cluster0"
        database_name = "MasterGrass"
        collection_name = "Terreno"
        client = pymongo.MongoClient(connection_string)

        try:
            db = client[database_name]
            col = db[collection_name]
            
            nuevo_terreno={
                "idTerreno": modelo_terreno.idTerreno,
                "ubicacion": {
                    "pais": modelo_terreno.ubicacion.pais,
                    "departamento": modelo_terreno.ubicacion.departamento,
                    "ciudad": modelo_terreno.ubicacion.ciudad,
                    "direccion": modelo_terreno.ubicacion.direccion
                },
                "tamano": modelo_terreno.tamano,
                "tipoPasto": modelo_terreno.tipoPasto,
                "precio": modelo_terreno.precio,
                "historialAlquileres": [
                    {
                        "idAlquiler": historial.idAlquiler,
                        "usuario":{
                            "idUsuario": historial.usuario.idUsuario,
                            "nombreUsuario": historial.usuario.nombreUsuario
                        }
                    }for historial in modelo_terreno.historialAlquileres
                ]

            }
            result = col.insert_one(nuevo_terreno)
            resultado = [f"Ingresar Terreno Exitoso: {result.acknowledged}"]
        except Exception as ex:
            resultado = f"Ingresar Terreno Fallido: {ex}"
        finally:
            client.close()
        
        return resultado

    
    #---------------------------------------------
    def modificar_terreno(self, id: str, modelo_terreno: ModeloTerreno):
        resultado = []
        connection_string = "mongodb+srv://mcorreace:sywv6ZiKRwQGwOJi@cluster0.55ale.mongodb.net/MasterGrass?retryWrites=true&w=majority&appName=Cluster0"
        database_name = "MasterGrass"
        collection_name = "Terreno"
        client = pymongo.MongoClient(connection_string)

        try:
            db = client[database_name]
            col = db[collection_name]

            result = col.update_one(
                {
                    "_id": ObjectId(id)
                },
                {
                    "$set": {
                        "idTerreno": modelo_terreno.idTerreno,
                        "ubicacion": {
                            "pais": modelo_terreno.ubicacion.pais,
                            "departamento": modelo_terreno.ubicacion.departamento,
                            "ciudad": modelo_terreno.ubicacion.ciudad,
                            "direccion": modelo_terreno.ubicacion.direccion
                        },
                        "tamano": modelo_terreno.tamano,
                        "tipoPasto": modelo_terreno.tipoPasto,
                        "precio": modelo_terreno.precio,
                        "historialAlquileres": [
                            {
                                "idAlquiler": historial.idAlquiler,
                                "usuario":{
                                    "idUsuario": historial.usuario.idUsuario,
                                    "nombreUsuario": historial.usuario.nombreUsuario
                                }
                            }for historial in modelo_terreno.historialAlquileres
                        ]

                    }
                }
            )

            resultado = f"Modificar Terreno Exitoso: acknowledged: {result.acknowledged}, modified_count: {result.modified_count}"
        except Exception as ex:
            resultado = f"Modificar Terreno Fallido: {ex}"
        finally:
            client.close()

        return resultado

    def eliminar_terreno(self, id:str):
        resultado = []
        connection_string = "mongodb+srv://mcorreace:sywv6ZiKRwQGwOJi@cluster0.55ale.mongodb.net/MasterGrass?retryWrites=true&w=majority&appName=Cluster0"
        database_name = "MasterGrass"
        collection_name = "Terreno"
        client = pymongo.MongoClient(connection_string)
        try:
            db = client[database_name]
            col = db[collection_name]
            result = col.delete_one(
                {
                    "_id": ObjectId(id)
                })
            resultado = [f"Eliminar Terreno Exitoso: {result.acknowledged, result.deleted_count}"]
        except Exception as ex:
            resultado = [f"Eliminar Terreno Fallido: {ex}"]
        finally:
            client.close()
        return resultado