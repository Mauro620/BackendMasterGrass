# apiusuario:
from fastapi import FastAPI, APIRouter, Depends, HTTPException
from Dominio.Usuario.modeloUsuario import ModeloUsuario, ModeloLogin, ModeloGanado
from Infraestructura.Usuario.infraestructuraUsuario import InfraestructuraUsuario
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import PyJWTError, ExpiredSignatureError, decode

from urllib.parse import unquote

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="usuario/login/")

app: FastAPI = FastAPI(
    title="API Usuario",
    description="Hola"
)

app = APIRouter()
# ----------------------------------------------------------------------------------------

def obtener_usuario_del_token(token: str = Depends(oauth2_scheme)):
    try:
        infraestructuraUsuario = InfraestructuraUsuario()
        payload = decode(token, infraestructuraUsuario.SECRET_KEY, algorithms=[infraestructuraUsuario.ALGORITHM])
        email = payload.get("sub")  # El "sub" es el email, esta en infraestructura crear token
        
        if email is None:
            raise HTTPException(status_code=401, detail="Usuario no encontrado en el token")
        
        return email

    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

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
# ---------------------- Consultar todos los usuarios ---------------------------
@app.get(
    "/verificar_usuario",
    response_model=list,
    summary="Consultar Usuario Todo",
    description="Consultar Usuario Todo",
    tags=["Usuario"]
)
async def verificar_usuario(email: str, contrasena:str):
    infraestructuraUsuario = InfraestructuraUsuario()
    return infraestructuraUsuario.verificar_usuario(email, contrasena)

# ------------------ Consultar usuario en especifico -------------------------

# Get
@app.get(
    "/consultar_usuario_email",
    response_model=list,	
    summary="Consultar Usuario email",
    description="Consultar Usuario email",
    tags=["Usuario"]
)
async def consultar_usuario_email(email:str):
    email_decoded = unquote(email)
    infraestructuraUsuario = InfraestructuraUsuario()
    return infraestructuraUsuario.consultar_usuario_email(email_decoded)


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

# ----------------------------------------------------------------
@app.post(
    "/login",
    summary="creartoken",
    description="Retirar Usuario",
    tags=["Usuario"]

)
async def login(modelologin: ModeloLogin):
    infraestructuraUsuario = InfraestructuraUsuario()
    
    # Verificar las credenciales del usuario
    usuario_valido = infraestructuraUsuario.verificar_usuario(modelologin.email, modelologin.contrasena)
    if usuario_valido[0] != "Usuario verificado correctamente":
        raise HTTPException(status_code=400, detail="Usuario o contraseña incorrectos")
    
    # Crear el token
    token = infraestructuraUsuario.crear_token({"email": modelologin.email})  
    return {"access_token": token, "token_type": "bearer"}

# --------------------------------------------------------------------

@app.get(
    "/perfil",
    summary="Obtener Perfil",
    description="Obtener Usuario usando token",
    tags=["Usuario"]
)
async def obtener_perfil(email: str = Depends(obtener_usuario_del_token)):
    # Aquí 'email' viene del token JWT decodificado en 'obtener_usuario_del_token'
    usuario = InfraestructuraUsuario().consultar_usuario_email(email)
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return usuario
# -------------------------------------------------------------------
@app.post(
    "/anadirterrenoausuario",
    summary="Obtener Perfil",
    description="Obtener Usuario usando token",
    tags=["Usuario"]
)
async def obtener_perfil(idUsuario, idTerreno):
    infraestructuraUsuario=InfraestructuraUsuario()
    return infraestructuraUsuario.agregar_terreno_a_usuario(idUsuario, idTerreno)
# -------------------------------------------------------------------
@app.post(
    "/anadirganadoausuario",
    summary="Obtener Perfil",
    description="Añadir ganado a un usuario",
    tags=["Usuario"]
)
async def obtener_perfil(idUsuario, modelo_ganado: ModeloGanado):
    infraestructuraUsuario=InfraestructuraUsuario()
    return infraestructuraUsuario.agregar_ganado_a_usuario(idUsuario, modelo_ganado)
