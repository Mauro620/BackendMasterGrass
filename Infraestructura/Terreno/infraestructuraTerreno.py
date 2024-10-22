from Dominio.Terreno.modeloTerreno import ModeloTerreno
from bson import ObjectId
import pymongo
from pymongo import MongoClient

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
            
            # Preparar el historial de alquileres si existe
            historial_alquileres = []
            if modelo_terreno.historialAlquileres:
                for alquiler in modelo_terreno.historialAlquileres:
                    historial_alquileres.append({
                        "idAlquiler": alquiler.idAlquiler,
                        "usuario": {
                            "idUsuario": alquiler.usuario.idUsuario,
                            "nombreUsuario": alquiler.usuario.nombreUsuario
                        },
                        "periodo": {
                            "fechaInicio": alquiler.periodo.fechaInicio,
                            "fechaFin": alquiler.periodo.fechaFin
                        }
                    })
            
            # Insertar los datos usando la estructura de tu ModeloTerreno
            result = col.insert_one(
                {
                    "idTerreno": modelo_terreno.idTerreno,
                    "ubicacion": {
                        "Pais": modelo_terreno.ubicacion.Pais,
                        "Departamento": modelo_terreno.ubicacion.Departamento,
                        "Ciudad": modelo_terreno.ubicacion.Ciudad,
                        "Direccion": modelo_terreno.ubicacion.Direccion
                    },
                    "tamano": modelo_terreno.tamano,
                    "tipoPasto": modelo_terreno.tipoPasto,
                    "precio": modelo_terreno.precio,
                    "estadoDelTerreno": modelo_terreno.estadoDelTerreno,
                    "historialAlquileres": historial_alquileres  # Se asigna el array construido
                }
            )
            resultado = f"Ingresar Terreno Exitoso: {result.acknowledged}"
        except Exception as ex:
            resultado = f"Ingresar Terreno Fallido: {ex}"
        finally:
            client.close()
        
        return resultado

    
    #---------------------------------------------
    def modificar_terreno(self, id:str, modelo_terreno: ModeloTerreno):
        resultado = []
        connection_string = "mongodb+srv://mcorreace:sywv6ZiKRwQGwOJi@cluster0.55ale.mongodb.net/MasterGrass?retryWrites=true&w=majority&appName=Cluster0"
        database_name = "MasterGrass"
        collection_name = "Terreno"
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
                    "IdTerreno": modelo_terreno.idTerreno,
                    "ubicacion": {
                        "Pais": modelo_terreno.ubicacion.Pais,
                        "Departamento": modelo_terreno.ubicacion.Departamento,
                        "Ciudad": modelo_terreno.ubicacion.Ciudad,
                        "Direccion": modelo_terreno.ubicacion.Direccion
                    },
                    "tamano": modelo_terreno.tamano,
                    "tipoPasto": modelo_terreno.tipoPasto,
                    "precio": modelo_terreno.precio,
                    "estadoDelTerreno": modelo_terreno.estadoDelTerreno,
                    "historialAlquileres": {
                        "idAlquiler": modelo_terreno.historialAlquileres.idAlquiler,
                        "usuario": {
                            "idUsuario": modelo_terreno.historialAlquileres.usuario.idUsuario,
                            "nombreUsuario": modelo_terreno.historialAlquileres.usuario.nombreUsuario
                        },
                        "periodo": {
                            "fechaInicio": modelo_terreno.historialAlquileres.periodo.fechaInicio,
                            "fechaFin": modelo_terreno.historialAlquileres.periodo.fechaFin
                        }
                    }
                }
                })
            resultado = f"Modificar Terreno Exitoso: {result.acknowledged, result.modified_count}"
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
            resultado = f"Eliminar Terreno Exitoso: {result.acknowledged, result.deleted_count}"
        except Exception as ex:
            resultado = f"Eliminar Terreno Fallido: {ex}"
        finally:
            client.close()
        return resultado