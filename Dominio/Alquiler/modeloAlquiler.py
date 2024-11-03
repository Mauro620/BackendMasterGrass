from pydantic import BaseModel
from bson import ObjectId
from typing import List, Optional
from datetime import datetime

class ModeloGanado(BaseModel):
    idGanado: str

class ModeloUsuario(BaseModel):
    idUsuario: str
    nombreUsuario: str
    email: str
    telefono: str
    ganado: List[ModeloGanado]

class ModeloPeriodo(BaseModel):
    fechaInicio: datetime
    fechaFin: datetime

    @classmethod
    def from_bson(cls, periodo):
        """Convierte fechas BSON a datetime correctamente."""
        fecha_inicio = periodo['fechaInicio']['$date'] if isinstance(periodo['fechaInicio'], dict) and '$date' in periodo['fechaInicio'] else periodo['fechaInicio']
        fecha_fin = periodo['fechaFin']['$date'] if isinstance(periodo['fechaFin'], dict) and '$date' in periodo['fechaFin'] else periodo['fechaFin']
        
        # Convertir a datetime si es necesario
        if isinstance(fecha_inicio, str):
            fecha_inicio = datetime.fromisoformat(fecha_inicio)
        if isinstance(fecha_fin, str):
            fecha_fin = datetime.fromisoformat(fecha_fin)

        return cls(
            fechaInicio=fecha_inicio,
            fechaFin=fecha_fin
        )

class ModeloTerreno(BaseModel):
    idTerreno: str
    precio: float

class ModeloAlquiler(BaseModel):
    _id: str  # ObjectId as string
    idAlquiler: str
    usuario: ModeloUsuario
    terreno: ModeloTerreno
    periodo: ModeloPeriodo
    tipoPago: str
    estadoTransaccion: str
    entidad: str
    precioTotal: float
    calificacion: Optional[int]

    @staticmethod
    def alquiler_helper(alquiler):
        return {
            "id": str(alquiler["_id"]), 
            "idAlquiler": str(alquiler["idAlquiler"]),
            "usuario": ModeloUsuario(
                idUsuario=str(alquiler['usuario']['idUsuario']),
                nombreUsuario=str(alquiler['usuario']['nombreUsuario']),
                email=str(alquiler['usuario']['email']),
                telefono=str(alquiler['usuario']['telefono']),
                ganado=[ModeloGanado(
                    idGanado=str(g['idGanado']),
                ) for g in alquiler['usuario']['ganado']]
            ),
            "terreno": ModeloTerreno(
                idTerreno=str(alquiler['terreno']['idTerreno']),
                precio=float(alquiler['terreno']['precio'])      
            ),
            "periodo": ModeloPeriodo.from_bson(alquiler['periodo']),
            "tipoPago": str(alquiler["tipoPago"]),
            "estadoTransaccion": str(alquiler["estadoTransaccion"]),
            "entidad": str(alquiler["entidad"]),
            "precioTotal": float(alquiler["precioTotal"]),
            "calificacion": alquiler.get("calificacion", None)  # Optional
        }
