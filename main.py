from fastapi import FastAPI
from routers.descargar_archivo import descarga_router
from routers.mostrar_ppal import mostrar_ppal_router

app = FastAPI()

app.include_router(descarga_router)
app.include_router(mostrar_ppal_router)