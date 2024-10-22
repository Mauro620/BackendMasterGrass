from fastapi import FastAPI, APIRouter

from Dominio.Alquiler.modeloAlquiler import ModeloAlquiler
from Infraestructura.Alquiler.infraestructuraAlquiler import InfraestructuraAlquiler

app: FastAPI = FastAPI(
    title="API Alquiler",
    description="Hola"
)

app = APIRouter()


# ---------------------- Consultar todos los alquileres ---------------------------
@app.get(
    "/consultar_ualquiler_todo",
    response_model=list,
    summary="Consultar Alquiler Todo",
    description="Consultar Alquiler Todo",
    tags=["Alquiler"]
)
async def consultar_alquiler_todo():
    infraestructuraAlquiler = InfraestructuraAlquiler()
    return infraestructuraAlquiler.consultar_alquiler_todo()

# ------------------ Consultar alquiler en especifico -------------------------

# Get
@app.get(
    "/consultar_alquiler_id",
    response_model=list,	
    summary="Consultar Alquiler Id",
    description="Consultar Alquiler Id",
    tags=["Alquiler"]
)
async def consultar_alquiler_id(id:str):
    infraestructuraAlquiler = InfraestructuraAlquiler()
    return infraestructuraAlquiler.consultar_alquiler_id(id)


# ------------------ Ingresar alquiler -------------------------

# Post
@app.post(
    "/ingresar_alquiler",
    summary="Ingresar Alquiler",
    description="Ingresar Alquiler",
    tags=["Alquiler"]
)
async def ingresar_alquiler(modeloalquiler: ModeloAlquiler):
    infraestructuraAlquiler = InfraestructuraAlquiler()
    return infraestructuraAlquiler.ingresar_alquiler(modeloalquiler)

# ------------------ Modificar alquiler -------------------------

#Metodo PUT
@app.put(
    "/modificar_alquiler",
    summary="Modificar Alquiler",
    description="Modificar Alquiler",
    tags=["Alquiler"]
)
async def modificar_alquiler(id:str, modeloalquiler: ModeloAlquiler):
    infraestructuraAlquiler = InfraestructuraAlquiler()
    return infraestructuraAlquiler.modificar_alquiler(id, modeloalquiler)

# ------------------ Remover un alquiler pasandole un id -------------------------

# Delete
@app.delete(
    "/eliminar_alquiler",
    summary="Retirar Alquiler",
    description="Retirar Alquiler",
    tags=["Alquiler"]
)
async def eliminar_alquiler(id:str):
    infraestructuraAlquiler = InfraestructuraAlquiler()
    return infraestructuraAlquiler.eliminar_alquiler(id)