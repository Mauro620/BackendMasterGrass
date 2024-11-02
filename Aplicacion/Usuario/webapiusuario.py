# apiusuario:

from fastapi import FastAPI, APIRouter

from Dominio.Usuario.modeloUsuario import ModeloUsuario
from Infraestructura.Usuario.infraestructuraUsuario import InfraestructuraUsuario

app: FastAPI = FastAPI(
    title="API Usuario",
    description="Hola"
)

app = APIRouter()
###################################

# ---------------------- Consultar todos los usuarios ---------------------------
@app.get(
    "/consultar_usuario_todo",
    response_model=list,
    summary="Consultar Usuario Todo",
    description="Consultar Usuario Todo",
    tags=["Usuario"]
)
async def consultar_usuario_todo():
    infraestructuraUsuario = InfraestructuraUsuario()
    return infraestructuraUsuario.consultar_usuario_todo()

# ------------------ Consultar usuario en especifico -------------------------

# Get
@app.get(
    "/consultar_usuario_id",
    response_model=list,	
    summary="Consultar Usuario Id",
    description="Consultar Usuario Id",
    tags=["Usuario"]
)
async def consultar_usuario_id(id:str):
    infraestructuraUsuario = InfraestructuraUsuario()
    return infraestructuraUsuario.consultar_usuario_id(id)


# ------------------ Ingresar usuario -------------------------

# Post
@app.post(
    "/ingresar_usuario",
    summary="Ingresar Usuario",
    description="Ingresar Usuario",
    tags=["Usuario"]
)
async def ingresar_usuario(modelousuario: ModeloUsuario):
    infraestructuraUsuario = InfraestructuraUsuario()
    return infraestructuraUsuario.ingresar_usuario(modelousuario)

# ------------------ Modificar usuario -------------------------

#Metodo PUT
@app.put(
    "/modificar_usuario",
    summary="Modificar Usuario",
    description="Modificar Usuario",
    tags=["Usuario"]
)
async def modificar_usuario(id:str, modelousuario: ModeloUsuario):
    infraestructuraUsuario = InfraestructuraUsuario()
    return infraestructuraUsuario.modificar_usuario (id, modelousuario)

# ------------------ Remover un usuario pasandole un id -------------------------

# Delete
@app.delete(
    "/eliminar_usuario",
    summary="Retirar Usuario",
    description="Retirar Usuario",
    tags=["Usuario"]
)
async def eliminar_usuario(id:str):
    infraestructuraUsuario = InfraestructuraUsuario()
    return infraestructuraUsuario.eliminar_usuario(id)
