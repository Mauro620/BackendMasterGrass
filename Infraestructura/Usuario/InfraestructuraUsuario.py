from Dominio.Usuario.modeloUsuario import ModeloUsuario
from bson import ObjectId
import pymongo
from typing import List
import bcrypt
import os
from fastapi import HTTPException, Depends
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext



#------------------ Usuario ------------------#
class InfraestructuraUsuario:

    def __init__(self) -> None:
        self.client = pymongo.MongoClient(os.getenv("connection_string"))
        self.db = self.client[os.getenv("database_name")]
        self.col = self.db["Usuario"]
        # Contexto para el hash de contraseñas
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        # Clave secreta para JWT (puedes guardarla en un archivo .env)
        self.SECRET_KEY = "mi_clave_secreta"  # Cambia esto por una clave más segura
        self.ALGORITHM = "HS256"


    #-------------------------------------------    
    def consultar_usuario_todo(self):
        results = []
        try:
            result = self.col.find()
            for item in list(result):
                results.append(ModeloUsuario.usuario_helper(item))
        
        except Exception as ex:
            print(f"Consultar Usuario Todo Fallido: {ex}")
        finally:
            self.client.close()
        return results
    #-------------------------------------------------------------------
    def consultar_usuario_email(self, email: str):
        resultado = []
        try:
            result = self.col.find_one(
                {
                    "email": str(email)
                })
            if result:  # Verificar si se encontró un documento
                resultado.append(ModeloUsuario.usuario_helper(result))
                print("Consultar Usuario email Exitoso")
            else:
                print("Usuario no encontrado")
                resultado = "Usuario no encontrado"
        except Exception as ex:
            resultado = f"Consultar Usuario email Fallido: {ex}"
        finally:
            self.client.close()
        return resultado
    # --------------------------------------------------------------------------------
    def ingresar_usuario(self, modelo_usuario: ModeloUsuario):
        resultado = []        
        try:
            # Hashear la contraseña usando bcrypt
            hashed_password = bcrypt.hashpw(modelo_usuario.contrasena.encode('utf-8'), bcrypt.gensalt())

            
            # Preparar la estructura para insertar
            nuevo_usuario = {
                "idUsuario": modelo_usuario.IdUsuario,
                "nombreUsuario": modelo_usuario.nombreUsuario,
                "email": modelo_usuario.email,
                "contrasena": hashed_password.decode('utf-8'),
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
            result = self.col.insert_one(nuevo_usuario)
            
            resultado = f"Ingresar Usuario Exitoso: {result.acknowledged}, ID insertado: {result.inserted_id}, tipo de objeto: {type(result)}"
        except Exception as ex:
            resultado = f"Ingresar Usuario Fallido: {ex}"
        finally:
            self.client.close()
        
        return resultado

    #---------------------------------------------
    def modificar_usuario(self, id:str, modelo_usuario: ModeloUsuario):
        resultado = []
        try:
            result = self.col.update_many(
                {
                    "_id": ObjectId(id)
                },
                {
                    "$set":
                    {
                    "idUsuario": modelo_usuario.IdUsuario,
                    "nombreUsuario": modelo_usuario.nombreUsuario,
                    "email": modelo_usuario.email,
                    "contrasena": modelo_usuario.contrasena,
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
            self.client.close()
        return resultado

    def eliminar_usuario(self, id:str):
        resultado = []
        try:
            result = self.col.delete_one(
                {
                    "_id": ObjectId(id)
                })
            resultado = f"Eliminar Usuario Exitoso: {result.acknowledged, result.deleted_count}"
        except Exception as ex:
            resultado = f"Eliminar Usuario Fallido: {ex}"
        finally:
            self.client.close()
        return resultado
    
    # -------------------- Verificar Usuario ----------------------------
    def verificar_usuario(self, email: str, contrasena: str):
        resultado = []
        try:
            # Buscar el usuario por email
            result = self.col.find_one({"email": email})

            if result:
                # Verificar la contraseña usando bcrypt
                if bcrypt.checkpw(contrasena.encode('utf-8'), result['contrasena'].encode('utf-8')):
                    resultado = ["Usuario verificado correctamente", result['email']]
                else:
                    resultado = ["Contraseña incorrecta"]
            else:
                resultado = ["Usuario no encontrado"]
        except Exception as ex:
            resultado = [f"Verificación de usuario fallida: {ex}"]
        finally:
            self.client.close()

        return resultado
    # ----------------------------------------------------
    def crear_token(self, data: dict):
        to_encode = data.copy()
        expiration = datetime.utcnow() + timedelta(hours=1)  # El token expirará en 1 hora
        to_encode.update({"exp": expiration, "sub": data.get("email")})
        return jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)

    # -----------------------------------------------------
    def verificar_usuario_y_crear_token(self, email: str, contrasena: str):
        try:
            # Buscar el usuario por email
            result = self.col.find_one({"email": email})

            if result:
                # Verificar la contraseña usando bcrypt
                if bcrypt.checkpw(contrasena.encode('utf-8'), result['contrasena'].encode('utf-8')):
                    # Generar token JWT
                    token = self.crear_token({"sub": result['email']})
                    return token  # Devolver el token al frontend
                else:
                    raise HTTPException(status_code=401, detail="Contraseña incorrecta")
            else:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
        except Exception as ex:
            raise HTTPException(status_code=500, detail=f"Error al verificar usuario: {ex}")
        
    # ------------------------------------------------------------
