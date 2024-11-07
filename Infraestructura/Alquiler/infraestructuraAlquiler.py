from Dominio.Alquiler.modeloAlquiler import ModeloAlquiler
from bson import ObjectId
import pymongo
from pymongo import MongoClient
import os

#------------------ Alquiler ------------------#
class InfraestructuraAlquiler:

    def __init__(self) -> None:
        self.client = pymongo.MongoClient(os.getenv("connection_string"))
        self.db = self.client[os.getenv("database_name")]
        self.col = self.db["Alquiler"]

    #-----------------------------------------    
    def consultar_alquiler_todo(self):
        results = []
        try:
            result = self.col.find()
            
            for item in list(result):
                results.append(ModeloAlquiler.alquiler_helper(item))
        
        except Exception as ex:
            print(f"Consultar Alquiler Todo Fallido: {ex}")
        finally:
            self.client.close()
        return results

#-------------------------------------------------------------------
    def consultar_alquiler_id(self, id:str):
        resultado = []
        try:
            result = self.col.find(
                {
                    "idAlquiler": id
                })
            for item in list(result):
                resultado.append(ModeloAlquiler.alquiler_helper(item))
            print(f"Consultar Alquiler Id Exitoso")
        except Exception as ex:
            resultado = f"Consultar Alquiler Id Fallido: {ex}"
        finally:
            self.client.close()
        return resultado
    

    # --------------------------------------------------------------------------------
    def ingresar_alquiler(self, modelo_Alquiler: ModeloAlquiler):
        resultado = []
        try:
            # Insertar los datos usando la estructura de tu ModeloAlquiler
            result = self.col.insert_one(
                {
                    "idAlquiler": modelo_Alquiler.idAlquiler,
                    "usuario": {
                        "idUsuario": modelo_Alquiler.usuario.idUsuario,
                        "nombreUsuario": modelo_Alquiler.usuario.nombreUsuario,
                        "email": modelo_Alquiler.usuario.email,
                        "telefono": modelo_Alquiler.usuario.telefono,
                        "ganado": [
                            {
                                "idGanado": g.idGanado
                            } for g in modelo_Alquiler.usuario.ganado
                        ]
                    },
                    "terreno": {
                        "idTerreno": modelo_Alquiler.terreno.idTerreno,
                        "precio": modelo_Alquiler.terreno.precio
                    },
                    "periodo": {
                        "fechaInicio": modelo_Alquiler.periodo.fechaInicio,
                        "fechaFin": modelo_Alquiler.periodo.fechaFin
                    },
                    "tipoPago": modelo_Alquiler.tipoPago,
                    "estadoTransaccion": modelo_Alquiler.estadoTransaccion,
                    "entidad": modelo_Alquiler.entidad,
                    "precioTotal": modelo_Alquiler.precioTotal,
                    "calificacion": modelo_Alquiler.calificacion
                }
            )

            resultado = f"Ingresar Alquiler Exitoso: {result.acknowledged}, ID insertado: {result.inserted_id}"
        except Exception as ex:
            resultado = f"Ingresar Alquiler Fallido: {ex}"
        finally:
            self.client.close()

        return resultado

    #---------------------------------------------
    def modificar_alquiler(self, id:str, modelo_Alquiler: ModeloAlquiler):
        resultado = []
        try:
            result = self.col.update_many(
                {
                    "_id": ObjectId(id)
                },
                {
                    "$set":
                    {
                    "idAlquiler": modelo_Alquiler.idAlquiler,
                    "usuario": {
                        "idUsuario": modelo_Alquiler.usuario.idUsuario,
                        "nombreUsuario": modelo_Alquiler.usuario.nombreUsuario,
                        "email": modelo_Alquiler.usuario.email,
                        "telefono": modelo_Alquiler.usuario.telefono,
                        "ganado": [
                            {
                                "idGanado": g.idGanado
                            } for g in modelo_Alquiler.usuario.ganado
                        ]
                    },
                    "terreno": {
                        "idTerreno": modelo_Alquiler.terreno.idTerreno,
                        "precio": modelo_Alquiler.terreno.precio
                    },
                    "periodo": {
                        "fechaInicio": modelo_Alquiler.periodo.fechaInicio,
                        "fechaFin": modelo_Alquiler.periodo.fechaFin
                    },
                    "tipoPago": modelo_Alquiler.tipoPago,
                    "estadoTransaccion": modelo_Alquiler.estadoTransaccion,
                    "entidad": modelo_Alquiler.entidad,
                    "precioTotal": modelo_Alquiler.precioTotal,
                    "calificacion": modelo_Alquiler.calificacion
                }
                })
            resultado = f"Modificar Alquiler Exitoso: {result.acknowledged, result.modified_count}"
        except Exception as ex:
            resultado = f"Modificar Alquiler Fallido: {ex}"
        finally:
            self.client.close()
        return resultado

    def eliminar_alquiler(self, id:str):
        resultado = []
        try:
            result = self.col.delete_one(
                {
                    "_id": ObjectId(id)
                })
            resultado = f"Eliminar Alquiler Exitoso: {result.acknowledged, result.deleted_count}"
        except Exception as ex:
            resultado = f"Eliminar Alquiler Fallido: {ex}"
        finally:
            self.client.close()
        return resultado