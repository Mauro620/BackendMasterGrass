from Dominio.Terreno.modeloTerreno import ModeloTerreno
from Infraestructura.Usuario.infraestructuraUsuario import InfraestructuraUsuario
from bson import ObjectId
import pymongo
import os
from azure.storage.blob import BlobServiceClient

#------------------ Terreno ------------------#
class InfraestructuraTerreno:

    def __init__(self) -> None:
        self.client = pymongo.MongoClient(os.getenv("connection_string"))
        self.db = self.client[os.getenv("database_name")]
        self.col = self.db["Terreno"]
        # AZURE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        # AZURE_CONTAINER_NAME = os.getenv("AZURE_CONTAINER_NAME")
        # self.blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
        # self.container_client = self.blob_service_client.get_container_client(AZURE_CONTAINER_NAME)
        
    def consultar_terreno_todo(self):
        results = []
        try:
            result = self.col.find()
            
            for item in list(result):
                results.append(ModeloTerreno.terreno_helper(item))
        
        except Exception as ex:
            print(f"Consultar Terreno Todo Fallido: {ex}")
        finally:
            self.client.close()
        return results

#-------------------------------------------------------------------
    def consultar_terreno_id(self, id:str):
        resultado = []
        try:
            result = self.col.find(
                {
                    "_id": ObjectId(id)
                })
            for item in list(result):
                resultado.append(ModeloTerreno.terreno_helper(item))
            print(f"Consultar Terreno Id Exitoso")
        except Exception as ex:
            resultado = f"Consultar Terreno Id Fallido: {ex}"
        finally:
            self.client.close()
        return resultado
    

    # --------------------------------------------------------------------------------
    def ingresar_terreno(self, modelo_terreno: ModeloTerreno, email: str):
        resultado = []
        try:            
            nuevo_terreno = {
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
                        "usuario": {
                            "idUsuario": historial.usuario.idUsuario,
                            "nombreUsuario": historial.usuario.nombreUsuario
                        }
                    } for historial in modelo_terreno.historialAlquileres
                ],
                "imagenes": modelo_terreno.imagenes
            }

            result = self.col.insert_one(nuevo_terreno)
            if result.acknowledged:
                # Agregar terreno al usuario usando el email
                infraestructura_usuario = InfraestructuraUsuario()
                usuario = infraestructura_usuario.consultar_usuario_email(email)
                
                if usuario and len(usuario) > 0:
                    id_usuario = usuario[0]['idUsuario']  # Asegúrate de obtener el primer usuario si es una lista
                    mensaje = infraestructura_usuario.agregar_terreno_a_usuario(id_usuario, modelo_terreno.idTerreno)
                    resultado = mensaje  # Mensaje de agregar terreno al usuario
                else:
                    resultado = ["Usuario no encontrado."]
            else:
                resultado = ["Error al ingresar terreno."]
        
        except Exception as ex:
            resultado = [f"Ingresar Terreno Fallido: {ex}"]
        finally:
            self.client.close()
        
        return resultado

    
    #---------------------------------------------
    def modificar_terreno(self, id: str, modelo_terreno: ModeloTerreno):
        resultado = []
        try:
            # Obtener el documento existente para preservar las imágenes antiguas
            terreno_existente = self.col.find_one({"_id": ObjectId(id)})
            imagenes_existentes = terreno_existente.get("imagenes")

            # Si hay imágenes nuevas, las agregamos, si no, mantenemos las existentes
            imagenes_actualizadas = modelo_terreno.imagenes if modelo_terreno.imagenes else imagenes_existentes

            result = self.col.update_one(
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
                                "usuario": {
                                    "idUsuario": historial.usuario.idUsuario,
                                    "nombreUsuario": historial.usuario.nombreUsuario
                                }
                            } for historial in modelo_terreno.historialAlquileres
                        ],
                        # Mantener las imágenes anteriores si no se envían nuevas
                        "imagenes": modelo_terreno.imagenes
                    }
                }
            )

            resultado = f"Modificar Terreno Exitoso: acknowledged: {result.acknowledged}, modified_count: {result.modified_count}"
        except Exception as ex:
            resultado = f"Modificar Terreno Fallido: {ex}"
        finally:
            self.client.close()

        return resultado


    def eliminar_terreno(self, id:str):
        resultado = []
        try:
            result = self.col.delete_one(
                {
                    "_id": ObjectId(id)
                })
            resultado = [f"Eliminar Terreno Exitoso: {result.acknowledged, result.deleted_count}"]
        except Exception as ex:
            resultado = [f"Eliminar Terreno Fallido: {ex}"]
        finally:
            self.client.close()
        return resultado