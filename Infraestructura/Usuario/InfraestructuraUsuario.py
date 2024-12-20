from Dominio.Usuario.modeloUsuario import ModeloUsuario, ModeloGanado
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
        # Clave secreta para JWT
        self.SECRET_KEY = "prueba" 
        self.ALGORITHM = "HS256"


    #------------------------------------- Consultar todos los usuarios -------------------------------    
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
    
    #------------------------------------- Consultar un usuario por email ------------------------------
    def consultar_usuario_email(self, email: str):
        resultado = []
        try:
            result = self.col.find_one(
                {
                    "email": str(email)
                })
            if result: 
                resultado.append(ModeloUsuario.usuario_helper(result))
                print("Consultar Usuario email Exitoso")
            else:
                print("Usuario no encontrado")
                resultado = "Usuario no encontrado"
        except Exception as ex:
            resultado = f"Consultar Usuario email Fallido: {ex}"
        finally:
            pass
        return resultado
    
    # ----------------------------------- Ingresar Usuario ---------------------------------------------
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

    #------------------------------------ Modificar Usuario --------------------------------------------
    # ASEGURATE DE CAMBIAR LA MODIFICACIÓN DE LA CONTRASEÑA DE FORMA CORRECTA
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

    # ----------------------------------- Eliminar usuario ---------------------------------------------
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
    
    # ----------------------------------- Verificar Usuario --------------------------------------------
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
    
    # ------------------------------------ Crear Token de Usuario --------------------------------------
    def crear_token(self, data: dict):
        to_encode = data.copy()
        expiration = datetime.utcnow() + timedelta(hours=1) 
        to_encode.update({"exp": expiration, "sub": data.get("email")})
        return jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)

    # ------------------------------------ Verificar y crear Token -------------------------------------
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
        
    # ------------------------------------ Ingresar un terreno a un usuario -------------------------------------
    def agregar_terreno_a_usuario(self, id_usuario: str, id_terreno: str):
        resultado = []
        try:
            # Actualiza el documento del usuario y agrega el idTerreno en el array 'terreno'
            result = self.col.update_one(
                {"idUsuario": id_usuario},
                {
                    "$push": {
                        "terreno": {"idTerreno": id_terreno}
                    }
                }
            )

            # Verifica si la operación fue exitosa
            if result.acknowledged:
                if result.modified_count > 0:
                    resultado = ["Terreno añadido exitosamente."]
                else:
                    # Si no se modificó nada, es posible que el terreno ya esté presente
                    resultado = ["El terreno ya estaba agregado o no se realizó ningún cambio."]
            else:
                resultado = ["La operación no fue reconocida por la base de datos."]
            
        except Exception as ex:
            print(f"Error al agregar terreno al usuario: {ex}")
            resultado = [f"Error al agregar terreno al usuario: {ex}"]
        finally:
            pass

        return resultado
    # --------------------------------- Ingresar Ganado a Usuario ----------------------------------------
    def agregar_ganado_a_usuario(self, id_usuario: str, modelo_usuario: ModeloGanado):
        resultado = []
        try:
            # Actualiza el documento del usuario y agrega el idTerreno en el array 'terreno'
            result = self.col.update_one(
                {"idUsuario": id_usuario},
                {
                    "$push": {
                        "ganado": {
                            "idGanado": modelo_usuario.idGanado,
                            "especie": modelo_usuario.especie,
                            "raza": modelo_usuario.raza,
                            "cantidad": modelo_usuario.cantidad,
                            "registrarCuidadoEspecial": [
                                {
                                "individuos": [
                                    {"serieIndividuo": ind}  # Extraer el valor del objeto ModeloIndividuo
                                    for ind in cu.individuos  # Recorre la lista de individuos en cada cuidado especial
                                    ],
                                    "tituloCaso": cu.tituloCaso,
                                    "descripcion": cu.descripcion
                                }
                                for cu in modelo_usuario.registrarCuidadoEspecial  # Recorre los cuidados especiales
                            ]
                        }      
                    }
                }
            )

            # Verifica si la operación fue exitosa
            if result.acknowledged:
                if result.modified_count > 0:
                    resultado = ["Ganado añadido exitosamente."]
                else:
                    # Si no se modificó nada, es posible que el terreno ya esté presente
                    resultado = ["El ganado ya estaba agregado o no se realizó ningún cambio."]
            else:
                resultado = ["La operación no fue reconocida por la base de datos."]
            
        except Exception as ex:
            print(f"Error al agregar ganado al usuario: {ex}")
            resultado = [f"Error al agregar ganado al usuario: {ex}"]
        finally:
            pass

        return resultado
