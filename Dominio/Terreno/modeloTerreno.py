from pydantic import BaseModel, Field
from bson import ObjectId
from typing import List
from datetime import datetime

class ModeloUbicacion(BaseModel):
    Pais: str
    Departamento: str
    Ciudad: str
    Direccion: str

class ModeloUsuario(BaseModel):
    idUsuario: str
    nombreUsuario: str

class ModeloPeriodo(BaseModel):
    fechaInicio: datetime
    fechaFin: datetime

class ModeloHistorialAlquileres(BaseModel):
    idAlquiler: str
    usuario: ModeloUsuario
    periodo: ModeloPeriodo

class ModeloTerreno(BaseModel):
    _id: ObjectId
    idTerreno: str = Field()
    ubicacion: ModeloUbicacion
    tamano: int  # Ahora es str, basado en tu documento
    tipoPasto: str
    precio: float  # Ahora es float, basado en tu documento
    historialAlquileres: List[ModeloHistorialAlquileres] # Lista de historial de alquileres
    
    @staticmethod
    def terreno_helper(terreno):
        return {
            "_id": str(terreno['_id']),
            "idTerreno": str(terreno['idTerreno']),
            "ubicacion": terreno['ubicacion'],  # Puedes utilizarlo directamente ya que es un diccionario
            "tamano": terreno['tamano'],
            "tipoPasto": terreno['tipoPasto'],
            "precio": terreno['precio'],
            "historialAlquileres": [
                {
                    "idAlquiler": alquiler["idAlquiler"],
                    "usuario": {
                        "idUsuario": alquiler["usuario"]["idUsuario"],
                        "nombreUsuario": alquiler["usuario"]["nombreUsuario"]
                    },
                    "periodo": {
                        "fechaInicio": alquiler["periodo"]["fechaInicio"],
                        "fechaFin": alquiler["periodo"]["fechaFin"],                        
                    }
                } for alquiler in terreno.get("historialAlquileres", []) 
            ]
        }

    @staticmethod
    def terreno_helper_ingresar(terreno):
        return {
            "_id": str(terreno['_id']),
            "idTerreno": str(terreno['idTerreno']),
            "ubicacion": terreno['ubicacion'],  # Puedes utilizarlo directamente ya que es un diccionario
            "tamano": terreno['tamano'],
            "tipoPasto": terreno['tipoPasto'],
            "precio": terreno['precio'],
            "estadoDelTerreno": terreno['estadoDelTerreno'],
            "historialAlquileres": [
                {
                    "idAlquiler": str(terreno["idAlquiler"]),
                    "usuario": {
                        "idUsuario": terreno["usuario"]["idUsuario"],
                        "nombreUsuario": terreno["usuario"]["nombreUsuario"]
                    },
                    "periodo": {
                        "fechaInicio": terreno["periodo"]["fechaInicio"],
                        "fechaFin": terreno["periodo"]["fechaFin"]
                    }
                }
            ]
        }, f"esto trae terreno.get {terreno.get}"