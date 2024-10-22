from fastapi import FastAPI, APIRouter

from Dominio.Terreno.modeloTerreno import ModeloTerreno
from Infraestructura.Terreno.infraestructuraTerreno import InfraestructuraTerreno

app: FastAPI = FastAPI(
    title= "API Terreno",
    description= "Hola"
)
app = APIRouter()

