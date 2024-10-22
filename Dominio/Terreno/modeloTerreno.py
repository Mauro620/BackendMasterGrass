from pydantic import BaseModel
from bson import ObjectId
from typing import List

class ModeloUbicacion(BaseModel):
    Pais: str
    Departamento: str
    Ciudad: str
    Direccion: str

class ModeloUsuario(BaseModel):
    idUsuario: str
    nombreUsuario: str

class ModeloPeriodo(BaseModel):
    fechaInicio: str
    fechaFin: str

class ModeloHistorialAlquileres(BaseModel):
    idAlquiler: str
    usuario: ModeloUsuario
    periodo: ModeloPeriodo

class ModeloTerreno(BaseModel):
    _id: str  # Convertido a str para asegurar serialización
    idTerreno: str
    ubicacion: ModeloUbicacion
    tamano: int  # Ahora es str, basado en tu documento
    tipoPasto: str
    precio: float  # Ahora es float, basado en tu documento
    estadoDelTerreno: str  # Corregido el nombre para reflejar tu documento
    historialAlquileres: List[ModeloHistorialAlquileres]  # Lista de historial de alquileres

    @staticmethod
    def terreno_helper(terreno):
        return {
            "_id": str(terreno['_id']),  # Convertir ObjectId a str
            "idTerreno": str(terreno['idTerreno']),
            "ubicacion": ModeloUbicacion(
                Pais=str(terreno['ubicacion']['Pais']),
                Departamento=str(terreno['ubicacion']['Departamento']),
                Ciudad=str(terreno['ubicacion']['Ciudad']),
                Direccion=str(terreno['ubicacion']['Direccion'])
            ),
            "tamano": int(terreno['tamano']),
            "tipoPasto": str(terreno['tipoPasto']),
            "precio": float(terreno['precio']),
            "estadoDelTerreno": str(terreno['estadoDelTerreno']),
            "historialAlquileres": ModeloHistorialAlquileres(
                idAlquiler= str(terreno["historialAlquileres"][0]["idAlquiler"]),
                usuario= ModeloUsuario(
                    idUsuario= str(terreno['historialAlquileres'][0]['usuario']['idUsuario']),
                    nombreUsuario= str(terreno['historialAlquileres'][0]['usuario']['nombreUsuario'])
                ),
                periodo=ModeloPeriodo(
                    fechaInicio= str(terreno['historialAlquileres'][0]['periodo']['fechaInicio']),
                    fechaFin= str(terreno['historialAlquileres'][0]['periodo']['fechaFin']),
                )
            )
        }
