from pydantic import BaseModel, Field
from bson import ObjectId
from typing import List
from datetime import datetime

class ModeloUbicacion(BaseModel):
    pais: str
    departamento: str
    ciudad: str
    direccion: str

class ModeloUsuario(BaseModel):
    idUsuario: str
    nombreUsuario: str

class ModeloPeriodo(BaseModel):
    fechaInicio: datetime
    fechaFin: datetime

    @classmethod
    def from_bson(cls, periodo):
        """Convierte fechas BSON a datetime correctamente."""
        # Verificar si 'fechaInicio' y 'fechaFin' son un diccionario con el formato BSON
        fecha_inicio = periodo['fechaInicio']['$date'] if isinstance(periodo['fechaInicio'], dict) and '$date' in periodo['fechaInicio'] else periodo['fechaInicio']
        fecha_fin = periodo['fechaFin']['$date'] if isinstance(periodo['fechaFin'], dict) and '$date' in periodo['fechaFin'] else periodo['fechaFin']
        
        # Verificar si las fechas ya son instancias de datetime o si necesitan conversión
        if isinstance(fecha_inicio, str):
            fecha_inicio = datetime.fromisoformat(fecha_inicio)
        if isinstance(fecha_fin, str):
            fecha_fin = datetime.fromisoformat(fecha_fin)

        return cls(
            fechaInicio=fecha_inicio,
            fechaFin=fecha_fin
        )

class ModeloHistorialAlquileres(BaseModel):
    idAlquiler: str
    usuario: ModeloUsuario
    periodo: ModeloPeriodo

class ModeloTerreno(BaseModel):
    _id: ObjectId
    idTerreno: str = Field()
    ubicacion: ModeloUbicacion
    tamano: int
    tipoPasto: str
    precio: float
    historialAlquileres: List[ModeloHistorialAlquileres]

    @staticmethod
    def terreno_helper(terreno):
        historial_alquileres = []
        
        for alquiler in terreno.get('historialAlquileres', []):
            try:
                periodo = alquiler['periodo']
                
                # Validar que el periodo es un diccionario antes de pasarlo al modelo
                if isinstance(periodo, dict):
                    historial_alquileres.append(
                        ModeloHistorialAlquileres(
                            idAlquiler=alquiler['idAlquiler'],
                            usuario=ModeloUsuario(
                                idUsuario=alquiler['usuario']['idUsuario'],
                                nombreUsuario=alquiler['usuario']['nombreUsuario']
                            ),
                            periodo=ModeloPeriodo.from_bson(periodo)
                        )
                    )
            except Exception as e:
                print(f"Error procesando historial de alquileres: {e}")

        return {
            "_id": str(terreno['_id']),
            "idTerreno": str(terreno['idTerreno']),
            "ubicacion": ModeloUbicacion(
                pais=terreno['ubicacion']['pais'],
                departamento=terreno['ubicacion']['departamento'],
                ciudad=terreno['ubicacion']['ciudad'],
                direccion=terreno['ubicacion']['direccion']
            ),
            "tamano": terreno['tamano'],
            "tipoPasto": terreno['tipoPasto'],
            "precio": terreno['precio'],
            "historialAlquileres": historial_alquileres
        }
