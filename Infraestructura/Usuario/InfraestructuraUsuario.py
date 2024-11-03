from Dominio.Usuario.modeloUsuario import ModeloUsuario
from bson import ObjectId
import pymongo
from pymongo import MongoClient
from typing import List

#------------------ Usuario ------------------#
class InfraestructuraUsuario:

    def __init__(self) -> None:
        pass

    #-------------------------------------------    
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
            
            # Preparar la estructura para insertar
            nuevo_usuario = {
                "idUsuario": modelo_usuario.IdUsuario,
                "nombreUsuario": modelo_usuario.nombreUsuario,
                "email": modelo_usuario.email,
                "telefono": modelo_usuario.telefono,
                "ganado": [
                    {
                        "idGanado": g.idGanado,
                        "especie": g.especie,
                        "raza": g.raza,
                        "cantidad": g.cantidad,
                        "registrarCuidadoEspecial": [
                        {
                            "individuos": [
                                        {"serieIndividuo": ind.serieIndividuo}  # Extraer el valor del objeto ModeloIndividuo
                                        for ind in cu.individuos  # Recorre la lista de individuos en cada cuidado especial
                                        ],
                                        "tituloCaso": cu.tituloCaso,
                                        "descripcion": cu.descripcion
                                    }
                                    for cu in g.registrarCuidadoEspecial  # Recorre los cuidados especiales
                                ]
                            }
                            for g in modelo_usuario.ganado
                        ],
                "terreno": [
                    {"idTerreno": t.idTerreno} for t in modelo_usuario.terreno
                ],
                "historialAlquileres": [
                    {
                        "idAlquiler": al.idAlquiler,
                        "idTerreno": al.idTerreno,
                        "fechaInicio": al.fechaInicio,
                        "fechaFin": al.fechaFin
                    }
                    for al in modelo_usuario.historialAlquileres
                ]
            }
            
            # Insertar el nuevo usuario en la colección
            result = col.insert_one(nuevo_usuario)
            
            resultado = f"Ingresar Usuario Exitoso: {result.acknowledged}, ID insertado: {result.inserted_id}, tipo de objeto: {type(result)}"
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
                    "idUsuario": modelo_usuario.IdUsuario,
                    "nombreUsuario": modelo_usuario.nombreUsuario,
                    "email": modelo_usuario.email,
                    "telefono": modelo_usuario.telefono,
                    "ganado": [
                        {
                            "idGanado": g.idGanado,
                            "especie": g.especie,
                            "raza": g.raza,
                            "cantidad": g.cantidad,
                            "registrarCuidadoEspecial": [
                            {
                                "individuos": [
                                            {"serieIndividuo": ind.serieIndividuo}  # Extraer el valor del objeto ModeloIndividuo
                                            for ind in cu.individuos  # Recorre la lista de individuos en cada cuidado especial
                                            ],
                                            "tituloCaso": cu.tituloCaso,
                                            "descripcion": cu.descripcion
                                        }
                                        for cu in g.registrarCuidadoEspecial  # Recorre los cuidados especiales
                                    ]
                                }
                                for g in modelo_usuario.ganado
                            ],
                    "terreno": [
                        {"idTerreno": t.idTerreno} for t in modelo_usuario.terreno
                    ],
                    "historialAlquileres": [
                        {
                            "idAlquiler": al.idAlquiler,
                            "idTerreno": al.idTerreno,
                            "fechaInicio": al.fechaInicio,
                            "fechaFin": al.fechaFin
                        }
                        for al in modelo_usuario.historialAlquileres
                    ]
                }       
                })
            resultado = f"Modificar Usuario Exitoso: {result.acknowledged, result.modified_count}"
        except Exception as ex:
            resultado = f"Modificar Usuario Fallido: {ex}"
        finally:
            client.close()
        return resultado

    def eliminar_usuario(self, id:str):
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