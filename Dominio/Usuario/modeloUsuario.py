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
    historialAlquileres: ModeloHistorialAlquiler
    

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
            "historialAlquileres": ModeloHistorialAlquiler(
                idAlquiler=str(usuario['historialAlquileres'][0]['idAlquiler']),  # Accedemos al primer elemento de la lista 'historialAlquileres'
                idTerreno=str(usuario['historialAlquileres'][0]['idTerreno']),
                fechaInicio=str(usuario['historialAlquileres'][0]['fechaInicio']),
                fechaFin=str(usuario['historialAlquileres'][0]['fechaFin'])
            )
        }
