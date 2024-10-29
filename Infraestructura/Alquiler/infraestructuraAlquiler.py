from Dominio.Alquiler.modeloAlquiler import ModeloAlquiler
from bson import ObjectId
import pymongo
from pymongo import MongoClient

#------------------ Alquiler ------------------#
class InfraestructuraAlquiler:

    def __init__(self) -> None:
        pass

    #-----------------------------------------    
    def consultar_alquiler_todo(self):
        results = []
        connection_string = "mongodb+srv://mcorreace:sywv6ZiKRwQGwOJi@cluster0.55ale.mongodb.net/MasterGrass?retryWrites=true&w=majority&appName=Cluster0"
        database_name = "MasterGrass"
        collection_name = "Alquiler"
        client = pymongo.MongoClient(connection_string)
        try:
            db = client[database_name]
            col = db[collection_name]
            result = col.find()
            
            for item in list(result):
                results.append(ModeloAlquiler.alquiler_helper(item))
        
        except Exception as ex:
            print(f"Consultar Alquiler Todo Fallido: {ex}")
        finally:
            client.close()
        return results

#-------------------------------------------------------------------
    def consultar_alquiler_id(self, id:str):
        resultado = []
        connection_string = "mongodb+srv://mcorreace:sywv6ZiKRwQGwOJi@cluster0.55ale.mongodb.net/MasterGrass?retryWrites=true&w=majority&appName=Cluster0"
        database_name = "MasterGrass"
        collection_name = "Alquiler"
        client = pymongo.MongoClient(connection_string)
        try:
            db = client[database_name]
            col = db[collection_name]
            result = col.find(
                {
                    "idAlquiler": id
                })
            for item in list(result):
                resultado.append(ModeloAlquiler.alquiler_helper(item))
            print(f"Consultar Alquiler Id Exitoso")
        except Exception as ex:
            resultado = f"Consultar Alquiler Id Fallido: {ex}"
        finally:
            client.close()
        return resultado
    

    # --------------------------------------------------------------------------------
    def ingresar_alquiler(self, modelo_Alquiler: ModeloAlquiler):
        resultado = []
        connection_string = "mongodb+srv://mcorreace:sywv6ZiKRwQGwOJi@cluster0.55ale.mongodb.net/MasterGrass?retryWrites=true&w=majority&appName=Cluster0"
        database_name = "MasterGrass"
        collection_name = "Alquiler"
        client = pymongo.MongoClient(connection_string)
        
        try:
            db = client[database_name]
            col = db[collection_name]
            
            # Insertar los datos usando la estructura de tu ModeloAlquiler
            result = col.insert_one(
                {
                    "IdAlquiler": modelo_Alquiler.idAlquiler,
                    "nombreAlquiler": modelo_Alquiler.nombreAlquiler,
                    "email": modelo_Alquiler.email,
                    "telefono": modelo_Alquiler.telefono,
                    "ubicacion": {
                        "Pais": modelo_Alquiler.ubicacion.Pais,
                        "Departamento": modelo_Alquiler.ubicacion.Pais,
                        "Pais": modelo_Alquiler.ubicacion.Pais,
                        "Pais": modelo_Alquiler.ubicacion.Pais,
                    },
                    "tipoAlquiler": modelo_Alquiler.tipoAlquiler,
                    "historialAlquileres": {
                        "idAlquiler": modelo_Alquiler.historialAlquileres.idAlquiler,
                        "idAlquiler": modelo_Alquiler.historialAlquileres.idAlquiler,
                        "fechaInicio": modelo_Alquiler.historialAlquileres.fechaInicio,
                        "fechaFin": modelo_Alquiler.historialAlquileres.fechaFin
                    }
                }
            )
            
            resultado = f"Ingresar Alquiler Exitoso: {result.acknowledged}, ID insertado: {result.inserted_id}"
        except Exception as ex:
            resultado = f"Ingresar Alquiler Fallido: {ex}"
        finally:
            client.close()
        
        return resultado
    #---------------------------------------------
    def modificar_alquiler(self, id:str, modelo_Alquiler: ModeloAlquiler):
        resultado = []
        connection_string = "mongodb+srv://mcorreace:sywv6ZiKRwQGwOJi@cluster0.55ale.mongodb.net/MasterGrass?retryWrites=true&w=majority&appName=Cluster0"
        database_name = "MasterGrass"
        collection_name = "Alquiler"
        client = pymongo.MongoClient(connection_string)
        try:
            db = client[database_name]
            col = db[collection_name]
            result = col.update_many(
                {
                    "_id": ObjectId(id)
                },
                {
                    "$set":
                    {
                    "IdAlquiler": modelo_Alquiler.IdAlquiler,
                    "nombreAlquiler": modelo_Alquiler.nombreAlquiler,
                    "email": modelo_Alquiler.email,
                    "telefono": modelo_Alquiler.telefono,
                    "ganado": {
                        "especie": modelo_Alquiler.ganado.especie,
                        "cantidad": modelo_Alquiler.ganado.cantidad,
                        "detalle": {
                            "idGanado": modelo_Alquiler.ganado.detalle.idGanado,
                            "raza": modelo_Alquiler.ganado.detalle.raza,
                            "estadoSalud": modelo_Alquiler.ganado.detalle.estadoSalud
                        }
                    },
                    "tipoAlquiler": modelo_Alquiler.tipoAlquiler,
                    "historialAlquileres": {
                        "idAlquiler": modelo_Alquiler.historialAlquileres.idAlquiler,
                        "idAlquiler": modelo_Alquiler.historialAlquileres.idAlquiler,
                        "fechaInicio": modelo_Alquiler.historialAlquileres.fechaInicio,
                        "fechaFin": modelo_Alquiler.historialAlquileres.fechaFin
                    }
                }
                })
            resultado = f"Modificar Alquiler Exitoso: {result.acknowledged, result.modified_count}"
        except Exception as ex:
            resultado = f"Modificar Alquiler Fallido: {ex}"
        finally:
            client.close()
        return resultado

    def eliminar_alquiler(self, id:str):
        resultado = []
        connection_string = "mongodb+srv://mcorreace:sywv6ZiKRwQGwOJi@cluster0.55ale.mongodb.net/MasterGrass?retryWrites=true&w=majority&appName=Cluster0"
        database_name = "MasterGrass"
        collection_name = "Alquiler"
        client = pymongo.MongoClient(connection_string)
        try:
            db = client[database_name]
            col = db[collection_name]
            result = col.delete_one(
                {
                    "_id": ObjectId(id)
                })
            resultado = f"Eliminar Alquiler Exitoso: {result.acknowledged, result.deleted_count}"
        except Exception as ex:
            resultado = f"Eliminar Alquiler Fallido: {ex}"
        finally:
            client.close()
        return resultado