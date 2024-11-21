from fastapi import FastAPI, APIRouter, Depends

from Dominio.Terreno.modeloTerreno import ModeloTerreno
from Infraestructura.Terreno.infraestructuraTerreno import InfraestructuraTerreno
from Aplicacion.Usuario.webApiusuario import obtener_usuario_del_token

app: FastAPI = FastAPI(
    title= "API Terreno",
    description= "Hola"
)
app = APIRouter() #Definir urls para incluir en el main
###################################

# ------------------ Consultar todos los terrenos -------------------------

@app.get(
    "/consultar_terrenos",
    tags=["Terreno"]
)
async def consultarTodosLosTerrenos():
    infraestructuraTerreno = InfraestructuraTerreno() 
    return infraestructuraTerreno.consultar_terreno_todo()
# ------------------ Consultar terreno en especifico -------------------------
@app.get(
    "/consultar_terreno_id",
    response_model= list,
    tags=["Terreno"]
)
async def consultarTerrenoId(id:str):
    infraestructuraTerreno = InfraestructuraTerreno()
    return infraestructuraTerreno.consultar_terreno_id(id)
# ------------------ Consultar terreno en especifico -------------------------
@app.get(
    "/filtrar_terrenos",
    response_model= list,
    tags=["Terreno"]
)
async def filtrarTerreno(
    ubicacion: str = None,
    precio_min: float = None,
    precio_max: float = None,
    tamano_min: float = None,
    tamano_max: float = None):
    infraestructuraTerreno = InfraestructuraTerreno()
    return infraestructuraTerreno.filtrar_terrenos(ubicacion, precio_min, precio_max,tamano_min, tamano_max)

# ------------------ Ingresar un nuevo terreno -------------------------
@app.post(
    "/ingresar_terreno",
    response_model= list,
    tags=["Terreno"]
)
async def ingresarTerreno(modeloTerreno: ModeloTerreno, email: str = Depends(obtener_usuario_del_token)):
    infraestructuraTerreno = InfraestructuraTerreno()
    return infraestructuraTerreno.ingresar_terreno(modeloTerreno, email)

# ------------------ Modificar un terreno seleccionado -------------------------
@app.put(
    "/modificar_terreno",
    tags=["Terreno"]
)
async def modificarTerreno(id:str, modeloTerreno : ModeloTerreno ):
    infraestructuraTerreno = InfraestructuraTerreno()
    return infraestructuraTerreno.modificar_terreno(id, modeloTerreno)

# ------------------ Remover un terreno pasandole un id -------------------------
@app.delete(
    "/eliminar_terreno",
    response_model= list,
    tags=['Terreno']
)
async def eliminarTerreno(id:str):
    infraestructuraTerreno = InfraestructuraTerreno()
    return infraestructuraTerreno.eliminar_terreno(id)