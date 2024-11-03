from pydantic import BaseModel
from bson import ObjectId
from datetime import datetime
from typing import List


class ModeloIndividuo(BaseModel):
    serieIndividuo: int

class ModeloTerreno(BaseModel):
    idTerreno: str

class ModeloCuidados(BaseModel):
    individuo: ModeloIndividuo
    tituloCaso: str
    descripcion: str

class ModeloGanado(BaseModel):
    idGanado: str
    especie: str
    raza: str
    cantidad: int
    registrarCuidadoEspecial: list[ModeloCuidados]

class ModeloHistorialAlquiler(BaseModel):
    idAlquiler: str
    idTerreno: str
    fechaInicio: datetime
    fechaFin: datetime

class ModeloUsuario(BaseModel):
    _id: ObjectId
    IdUsuario: str
    nombreUsuario: str
    email: str
    contraseña: str
    telefono: str
    ganado: list[ModeloGanado]
    terreno: list[ModeloTerreno]
    historialAlquileres: list[ModeloHistorialAlquiler]  # Ahora es una lista de historial de alquileres

    @staticmethod
    def usuario_helper(usuario):
        ganado = [
            ModeloGanado(
                idGanado=str(g['idGanado']),
                especie=str(g['especie']),
                raza=str(g['raza']),
                cantidad=g['cantidad'],
                registrarCuidadoEspecial=[
                    ModeloCuidados(
                        individuo=ModeloIndividuo(serieIndividuo=int(ind['serieIndividuo'])),
                        tituloCaso=str(c['tituloCaso']),
                        descripcion=str(c['descripcion'])
                    ) for c in g.get('registrarCuidadoEspecial', [])
                    for ind in c.get('individuos', [])
                ]
            ) for g in usuario.get('ganado', [])
        ]

        # Convierte las fechas de string a datetime
        # fecha_inicio = datetime(usuario['historialAlquileres'][0]['fechaInicio'], '%Y-%m-%dT%H:%M:%S.%fZ') if 'historialAlquileres' in usuario and usuario['historialAlquileres'] else None
        # fecha_fin = datetime(usuario['historialAlquileres'][0]['fechaFin'], '%Y-%m-%dT%H:%M:%S.%fZ') if 'historialAlquileres' in usuario and usuario['historialAlquileres'] else None

        return {
            "_id": str(usuario['_id']),
            "idUsuario": str(usuario.get('idUsuario', '')),
            "nombreUsuario": str(usuario['nombreUsuario']),
            "email": str(usuario['email']),
            "telefono": str(usuario['telefono']),
            "ganado": ganado,
            "terreno": [
                ModeloTerreno(idTerreno=str(t['idTerreno'])) for t in usuario.get('terreno', [])
            ],
            "historialAlquileres": [
                ModeloHistorialAlquiler(
                    idAlquiler=str(alquiler['idAlquiler']),
                    idTerreno=str(alquiler['idTerreno']),
                    fechaInicio=datetime(alquiler['fechaInicio'], '%Y-%m-%dT%H:%M:%S.%fZ') if isinstance(alquiler['fechaInicio'], str) else alquiler['fechaInicio'],
                    fechaFin=datetime(alquiler['fechaFin'], '%Y-%m-%dT%H:%M:%S.%fZ') if isinstance(alquiler['fechaFin'], str) else alquiler['fechaFin']
                ) for alquiler in usuario.get('historialAlquileres', [])
            ]
        }


