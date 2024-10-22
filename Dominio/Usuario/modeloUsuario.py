from pydantic import BaseModel
from bson import ObjectId


class ModeloDetalle(BaseModel):
    idGanado: str
    raza: str
    estadoSalud: str

class ModeloGanado(BaseModel):
    especie: str
    cantidad: str
    detalle: ModeloDetalle

class ModeloHistorialAlquiler(BaseModel):
    idAlquiler: str
    idTerreno: str
    fechaInicio: str 
    fechaFin: str

class ModeloUsuario(BaseModel):
    _id: ObjectId
    IdUsuario: str
    nombreUsuario: str
    email: str
    telefono: str
    ganado: ModeloGanado
    tipoUsuario: str
    historialAlquileres: list[ModeloHistorialAlquiler]  # Ahora es una lista de historial de alquileres
    

    @staticmethod
    def usuario_helper(usuario):
        return {
            "_id": str(usuario['_id']),
            "idUsuario": str(usuario['idUsuario']),
            "nombreUsuario": str(usuario['nombreUsuario']),
            "email": str(usuario['email']),
            "telefono": str(usuario['telefono']),
            "ganado": ModeloGanado(
                especie=str(usuario['ganado'][0]['especie']),  # Accedemos al primer elemento de la lista 'ganado'
                cantidad=str(usuario['ganado'][0]['cantidad']),
                detalle=ModeloDetalle(
                    idGanado=str(usuario['ganado'][0]['detalle'][0]['idGanado']),  # Accedemos al primer elemento de la lista 'detalle'
                    raza=str(usuario['ganado'][0]['detalle'][0]['raza']),
                    estadoSalud=str(usuario['ganado'][0]['detalle'][0]['estadoSalud'])
                )
            ),
            "tipoUsuario": str(usuario['tipoUsuario']),
            "historialAlquileres": [  # Iteramos sobre la lista de 'historialAlquileres'
                ModeloHistorialAlquiler(
                    idAlquiler=str(alquiler['idAlquiler']),
                    idTerreno=str(alquiler['idTerreno']),
                    fechaInicio=str(alquiler['fechaInicio']),
                    fechaFin=str(alquiler['fechaFin'])
                ) for alquiler in usuario['historialAlquileres']
            ]
        }
