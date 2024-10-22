# apiusuario:

from fastapi import FastAPI, APIRouter

from Dominio.Usuario.modeloUsuario import ModeloUsuario
from Infraestructura.Usuario.infraestructuraUsuario import InfraestructuraUsuarioPene

app: FastAPI = FastAPI(
    title="API Usuario",
    description="Hola"
)

app = APIRouter()
###################################

# ---------------------- Consultar Todo ---------------------------
@app.get(
    "/consultarusuariotodo",
    response_model=list,
    summary="Consultar Usuario Todo",
    description="Consultar Usuario Todo",
    tags=["Usuario"]
)
async def consultar_usuario_todo():
    infraestructurausuario = InfraestructuraUsuarioPene()
    return infraestructurausuario.consultar_usuario_todo()

###################################

# Get
@app.get(
    "/consultarusuarioid",
    response_model=list,	
    summary="Consultar Usuario Id",
    description="Consultar Usuario Id",
    tags=["Usuario"]
)
async def consultar_usuario_id(id:str):
    infraestructurausuario = InfraestructuraUsuarioPene()
    return infraestructurausuario.consultar_usuario_id(id)


###################################

# Post
@app.post(
    "/ingresarusuario",
    summary="Ingresar Usuario",
    description="Ingresar Usuario",
    tags=["Usuario"]
)
async def ingresar_usuario(modelousuario: ModeloUsuario):
    infraestructurausuario = InfraestructuraUsuarioPene()
    return infraestructurausuario.ingresar_usuario(modelousuario)

###################################

#Metodo PUT
@app.put(
    "/modificarusuario",
    summary="Modificar Usuario",
    description="Modificar Usuario",
    tags=["Usuario"]
)
async def modificar_usuario(id:str, modelousuario: ModeloUsuario):
    infraestructurausuario = InfraestructuraUsuarioPene()
    return infraestructurausuario.modificar_usuario (id, modelousuario)

###################################
