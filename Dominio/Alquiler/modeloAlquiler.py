from pydantic import BaseModel
from bson import ObjectId
from typing import List

class ModeloGanado(BaseModel):
    especie: str
    cantidad: int

class ModeloUsuario(BaseModel):
    idUsuario: str
    nombreUsuario: str
    email: str
    telefono: str
    ganado: List[ModeloGanado]

class ModeloPeriodo(BaseModel):
    fechaInicio: str
    fechaFin: str

class ModeloTerreno(BaseModel):
    idTerreno: str
    precio: float

class ModeloAlquiler(BaseModel):
    id: str  # ObjectId as string
    idAlquiler: str
    usuario: ModeloUsuario
    terreno: ModeloTerreno
    periodo: ModeloPeriodo
    pagoTotal: float

    @staticmethod
    def alquiler_helper(alquiler):
        return {
            "id": str(alquiler["_id"]),  # Convert ObjectId to string
            "idAlquiler": str(alquiler["idAlquiler"]),
            "usuario": ModeloUsuario(
                idUsuario=str(alquiler['usuario']['idUsuario']),
                nombreUsuario=str(alquiler['usuario']['nombreUsuario']),
                email=str(alquiler['usuario']['email']),
                telefono=str(alquiler['usuario']['telefono']),
                ganado=[ModeloGanado(
                    especie=str(g['especie']),
                    cantidad=int(g['cantidad'])
                ) for g in alquiler['usuario']['ganado']]
            ),
            "terreno": ModeloTerreno(
                idTerreno=str(alquiler['terreno']['idTerreno']),
                precio=float(alquiler['terreno']['precio'])      
            ),
            "periodo": ModeloPeriodo(
                fechaInicio=str(alquiler['periodo']['fechaInicio']),
                fechaFin=str(alquiler['periodo']['fechaFin'])
            ),
            "pagoTotal": float(alquiler["pagoTotal"])
        }
