from Dominio.Usuario.modeloUsuario import ModeloUsuario
from bson import ObjectId
import pymongo
from pymongo import MongoClient

#------------------ Usuario ------------------#
class InfraestructuraUsuarioPene:

    def __init__(self) -> None:
        pass
        
    def consultar_usuario_todo(self):
        results = []
        connection_string = "mongodb+srv://mcorreace:sywv6ZiKRwQGwOJi@cluster0.55ale.mongodb.net/MasterGrass?retryWrites=true&w=majority&appName=Cluster0"
        database_name = "MasterGrass"
        collection_name = "Usuario"
        client = pymongo.MongoClient(connection_string)
        try:
            db = client[database_name]
            col = db[collection_name]
            result = col.find()
            
            for item in list(result):
                results.append(ModeloUsuario.usuario_helper(item))
        
        except Exception as ex:
            print(f"Consultar Usuario Todo Fallido: {ex}")
        finally:
            client.close()
        return results

#-------------------------------------------------------------------
    def consultar_usuario_id(self, id:str):
        resultado = []
        connection_string = "mongodb+srv://mcorreace:sywv6ZiKRwQGwOJi@cluster0.55ale.mongodb.net/MasterGrass?retryWrites=true&w=majority&appName=Cluster0"
        database_name = "MasterGrass"
        collection_name = "Usuario"
        client = pymongo.MongoClient(connection_string)
        try:
            db = client[database_name]
            col = db[collection_name]
            result = col.find(
                {
                    "idUsuario": id
                })
            for item in list(result):
                resultado.append(ModeloUsuario.usuario_helper(item))
            print(f"Consultar Usuario Id Exitoso")
        except Exception as ex:
            resultado = f"Consultar Usuario Id Fallido: {ex}"
        finally:
            client.close()
        return resultado
    

    # --------------------------------------------------------------------------------
    def ingresar_usuario(self, modelo_usuario: ModeloUsuario):
        resultado = []
        connection_string = "mongodb+srv://mcorreace:sywv6ZiKRwQGwOJi@cluster0.55ale.mongodb.net/MasterGrass?retryWrites=true&w=majority&appName=Cluster0"
        database_name = "MasterGrass"
        collection_name = "Usuario"
        client = pymongo.MongoClient(connection_string)
        
        try:
            db = client[database_name]
            col = db[collection_name]
            
            # Insertar los datos usando la estructura de tu ModeloUsuario
            result = col.insert_one(
                {
                    "IdUsuario": modelo_usuario.IdUsuario,
                    "nombreUsuario": modelo_usuario.nombreUsuario,
                    "email": modelo_usuario.email,
                    "telefono": modelo_usuario.telefono,
                    "ganado": {
                        "especie": modelo_usuario.ganado.especie,
                        "cantidad": modelo_usuario.ganado.cantidad,
                        "detalle": {
                            "idGanado": modelo_usuario.ganado.detalle.idGanado,
                            "raza": modelo_usuario.ganado.detalle.raza,
                            "estadoSalud": modelo_usuario.ganado.detalle.estadoSalud
                        }
                    },
                    "tipoUsuario": modelo_usuario.tipoUsuario,
                    "historialAlquileres": {
                        "idAlquiler": modelo_usuario.historialAlquileres.idAlquiler,
                        "idTerreno": modelo_usuario.historialAlquileres.idTerreno,
                        "fechaInicio": modelo_usuario.historialAlquileres.fechaInicio,
                        "fechaFin": modelo_usuario.historialAlquileres.fechaFin
                    }
                }
            )
            
            resultado = f"Ingresar Usuario Exitoso: {result.acknowledged}, ID insertado: {result.inserted_id}"
        except Exception as ex:
            resultado = f"Ingresar Usuario Fallido: {ex}"
        finally:
            client.close()
        
        return resultado
    #---------------------------------------------
    def modificar_usuario(self, id:str, modelo_usuario: ModeloUsuario):
        resultado = []
        connection_string = "mongodb+srv://mcorreace:sywv6ZiKRwQGwOJi@cluster0.55ale.mongodb.net/MasterGrass?retryWrites=true&w=majority&appName=Cluster0"
        database_name = "MasterGrass"
        collection_name = "Usuario"
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
                    "IdUsuario": modelo_usuario.IdUsuario,
                    "nombreUsuario": modelo_usuario.nombreUsuario,
                    "email": modelo_usuario.email,
                    "telefono": modelo_usuario.telefono,
                    "ganado": {
                        "especie": modelo_usuario.ganado.especie,
                        "cantidad": modelo_usuario.ganado.cantidad,
                        "detalle": {
                            "idGanado": modelo_usuario.ganado.detalle.idGanado,
                            "raza": modelo_usuario.ganado.detalle.raza,
                            "estadoSalud": modelo_usuario.ganado.detalle.estadoSalud
                        }
                    },
                    "tipoUsuario": modelo_usuario.tipoUsuario,
                    "historialAlquileres": {
                        "idAlquiler": modelo_usuario.historialAlquileres.idAlquiler,
                        "idTerreno": modelo_usuario.historialAlquileres.idTerreno,
                        "fechaInicio": modelo_usuario.historialAlquileres.fechaInicio,
                        "fechaFin": modelo_usuario.historialAlquileres.fechaFin
                    }
                }
                })
            resultado = f"Modificar Usuario Exitoso: {result.acknowledged, result.modified_count}"
        except Exception as ex:
            resultado = f"Modificar Usuario Fallido: {ex}"
        finally:
            client.close()
        return resultado

    def retirar_usuario(self, id:str):
        resultado = []
        connection_string = "mongodb+srv://mcorreace:sywv6ZiKRwQGwOJi@cluster0.55ale.mongodb.net/MasterGrass?retryWrites=true&w=majority&appName=Cluster0"
        database_name = "MasterGrass"
        collection_name = "Usuario"
        client = pymongo.MongoClient(connection_string)
        try:
            db = client[database_name]
            col = db[collection_name]
            result = col.delete_one(
                {
                    "_id": ObjectId(id)
                })
            resultado = f"Eliminar Usuario Exitoso: {result.acknowledged, result.deleted_count}"
        except Exception as ex:
            resultado = f"Eliminar Usuario Fallido: {ex}"
        finally:
            client.close()
        return resultado