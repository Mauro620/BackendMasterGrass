import uvicorn
from fastapi import FastAPI

from Aplicacion.Usuario.webapiusuario import app as RutaUsuario
from Aplicacion.Terreno.webApiTerreno import app as RutaTerreno

# Inicializar FastAPi
app = FastAPI()

# Incluimos las rutas dadas en los archivos de API para incluirlos en una sola pagina en fastapi
app.include_router(RutaUsuario, prefix="/usuario")
app.include_router(RutaTerreno, prefix="/terreno")

# Funcion para iniciar fastapi con nuestros parametros desde le archivo main
def start():
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8070,
        reload=True
    )

if __name__ == '__main__':
    start()
