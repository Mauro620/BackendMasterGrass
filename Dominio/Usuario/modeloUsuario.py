from pydantic import BaseModel
from bson import ObjectId
from datetime import datetime
from typing import List,Optional

class ModeloIndividuo(BaseModel):
    serieIndividuo: int

class ModeloTerreno(BaseModel):
    idTerreno: str

class ModeloCuidados(BaseModel):
    individuos: list[ModeloIndividuo] 
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

class ModeloLogin(BaseModel):
    email: str
    contrasena: str


class ModeloUsuario(BaseModel):
    _id: ObjectId
    IdUsuario: str
    nombreUsuario: str
    email: str
    contrasena: str
    telefono: str
    ganado: Optional[list[ModeloGanado]] = []
    terreno: Optional[list[ModeloTerreno]] = []
    historialAlquileres: Optional[list[ModeloHistorialAlquiler]] =[]
    

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
                        individuos=[
                            ModeloIndividuo(serieIndividuo=int(ind['serieIndividuo'])) for ind in c.get('individuos', [])
                        ],
                        tituloCaso=str(c['tituloCaso']),
                        descripcion=str(c['descripcion'])
                    ) for c in g.get('registrarCuidadoEspecial', [])
                ]
            ) for g in usuario.get('ganado', [])
        ]

        return {
            "idUsuario": str(usuario.get('idUsuario', '')),
            "nombreUsuario": str(usuario['nombreUsuario']),
            "email": str(usuario['email']),
            "contrasena": str(usuario['contrasena']),
            "telefono": str(usuario['telefono']),
            "ganado": ganado,
            "terreno": [
                ModeloTerreno(idTerreno=str(t['idTerreno'])) for t in usuario.get('terreno', [])
            ],
            "historialAlquileres": [
                ModeloHistorialAlquiler(
                    idAlquiler=str(alquiler['idAlquiler']),
                    idTerreno=str(alquiler['idTerreno']),
                    fechaInicio=datetime.fromisoformat(alquiler['fechaInicio']) if isinstance(alquiler['fechaInicio'], str) else alquiler['fechaInicio'],
                    fechaFin=datetime.fromisoformat(alquiler['fechaFin']) if isinstance(alquiler['fechaFin'], str) else alquiler['fechaFin']
                ) for alquiler in usuario.get('historialAlquileres', [])
            ]
        }
