
from google.cloud import storage
from google.oauth2 import service_account
from fastapi import APIRouter
from models import DownloadData
import pandas as pd
bucket_name = 'review_main_cities'
archivo_dict = {
            'New York': {'positivos': 'comentarios_positivos_NY.csv', 'negativos': 'comentarios_negativos_NY.csv'},
            'California': {'positivos': 'comentarios_positivos_CA.csv', 'negativos': 'comentarios_negativos_CA.csv'},
            'Florida': {'positivos': 'comentarios_positivos_FL.csv', 'negativos': 'comentarios_negativos_FL.csv'},
            'Texas': {'positivos': 'comentarios_positivos_TX.csv', 'negativos': 'comentarios_negativos_TX.csv'}
        }

credentials = service_account.Credentials.from_service_account_file(
    'env/utopian-honor-438417-u7-5b7f84fcfd25.json'
)

client = storage.Client(project='utopian-honor-438417-u7', credentials=credentials)

descarga_router = APIRouter()

@descarga_router.post("/download")
def descargar_archivo(data: DownloadData):
    ciudad = archivo_dict[data.ciudad]
    archivo_name = ciudad[data.opinion]

    try:
        bucket = client.get_bucket(bucket_name)# Obtener bucket y blob
        blob = bucket.blob(archivo_name)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as temp_file:# Crear archivo temporal
            # Descargar blob al archivo temporal
            blob.download_to_filename(temp_file.name)
            
            df = pd.read_csv(temp_file.name)# Leer con pandas
        
        return df# El archivo temporal se eliminará automáticamente
    
    except Exception as e:
        print(f"Error al descargar: {e}")
        return None