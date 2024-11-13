import os
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
from uuid import uuid4
from fastapi import UploadFile, HTTPException, FastAPI, APIRouter
import pymongo
from bson import ObjectId

app: FastAPI = FastAPI(
    title="Imagenes",
    description="hola"
)
app = APIRouter()

# Cargar variables de entorno
load_dotenv()

# Datos de conexión de Azure
AZURE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
AZURE_CONTAINER_NAME = os.getenv("AZURE_CONTAINER_NAME")

# Datos de conexión de mongo
collection_name = "Terreno"
client = pymongo.MongoClient(os.getenv("connection_string"))
db = client[os.getenv("database_name")]
col = db["Terreno"]

# Crear el cliente de Blob Storage
blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(AZURE_CONTAINER_NAME)

# ------------------- Cargar Imagenes ------------------
@app.post("/upload/{terreno_id}")
async def upload_image(file: UploadFile, terreno_id: str):
    try:
        print(f"Connection String: {AZURE_CONNECTION_STRING}")
        file_name = f"{uuid4()}-{file.filename}"
        
        blob_client = container_client.get_blob_client(file_name)
        blob_client.upload_blob(file.file)

        file_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{AZURE_CONTAINER_NAME}/{file_name}"
        result = col.update_one(
            {"idTerreno": str(terreno_id)}, 
            {"$push": {"imagenes": file_url}} 
        )

        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Terreno no encontrado")
        
        return {"message": "Imagen subida y URL guardada", "file_url": file_url}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al subir el archivo: {str(e)}")

# --------------------- Listar Imagenes ------------------------
@app.get("/terreno/{terreno_id}/imagenes")
async def get_terreno_images(terreno_id: str):
    try:
        terreno = col.find_one({"_id": ObjectId(terreno_id)})

        if not terreno:
            raise HTTPException(status_code=404, detail="Terreno no encontrado")

        return {"imagenes": terreno.get("imagenes", [])}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener las imágenes: {str(e)}")

# ---------------------- Modificar Imagenes ----------------------
@app.put("/update/{file_name}")
async def update_image(file_name: str, file: UploadFile):
    try:
        # Sobrescribir el blob existente con el nuevo archivo
        blob_client = container_client.get_blob_client(file_name)
        blob_client.upload_blob(file.file, overwrite=True)

        return {"message": f"Imagen {file_name} actualizada exitosamente"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar la imagen: {str(e)}")

# ---------------------- Eliminar Imagen --------------------------
@app.delete("/terreno/{terreno_id}/imagenes/{file_name}")
async def delete_image(terreno_id: str, file_name: str):
    try:
        # Eliminar la imagen de Azure Blob Storage
        blob_client = container_client.get_blob_client(file_name)
        blob_client.delete_blob()

        # Eliminar la URL de la imagen de la base de datos
        result = col.update_one(
            {"_id": ObjectId(terreno_id)},
            {"$pull": {"imagenes": f"https://{blob_service_client.account_name}.blob.core.windows.net/{AZURE_CONTAINER_NAME}/{file_name}"}}
        )

        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Terreno no encontrado")

        return {"message": "Imagen eliminada exitosamente"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar la imagen: {str(e)}")

