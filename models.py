from pydantic import BaseModel
import pandas as pd

class DownloadData(BaseModel):
    opinion:str
    ciudad:str

class ShowData(BaseModel):
    resenias:pd.DataFrame
    tipo:str

    class Config:
        arbitrary_types_allowed = True

class TextoData(BaseModel):
    resenia_negativa:pd.DataFrame

    class Config:
        arbitrary_types_allowed = True

class ProcesarData(BaseModel):
    resenias:pd.DataFrame
    tipo:str

    class Config:
        arbitrary_types_allowed = True