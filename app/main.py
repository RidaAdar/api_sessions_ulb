from fastapi import FastAPI
from fastapi.responses import JSONResponse
import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta
import asyncio

app = FastAPI()
fake = Faker('fr_FR')

# Charger les étudiants
etudiants = pd.read_csv("etudiants.csv")
salles = [f"S{str(i).zfill(3)}" for i in range(1, 21)]

sessions = []

# Générateur toutes les 30 secondes
async def generate_sessions():
    while True:
        etudiant = etudiants.sample(1).iloc[0]
        now = datetime.utcnow()
        session = {
            "id_session": f"sess_{len(sessions)+1:04d}",
            "id_etudiant": int(etudiant["id"]),
            "debut": now.isoformat(),
            "fin": (now + timedelta(minutes=random.randint(30, 120))).isoformat(),
            "id_salle": random.choice(salles)
        }
        sessions.append(session)
        await asyncio.sleep(30)

@app.on_event("startup")
async def start_session_generator():
    asyncio.create_task(generate_sessions())

@app.get("/sessions")
def get_sessions():
    return JSONResponse(content=sessions)
