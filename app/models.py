from pydantic import BaseModel

class Session(BaseModel):
    id_session: str
    id_etudiant: int
    debut: str
    fin: str
    id_salle: str
