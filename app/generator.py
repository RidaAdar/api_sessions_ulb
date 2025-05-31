import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta
import asyncio

from app.models import Session

fake = Faker('fr_FR')
etudiants = pd.read_csv("data/etudiants.csv")

salles = [f"S{str(i).zfill(3)}" for i in range(1, 21)]

sessions = []

async def generate_sessions():
    while True:
        etudiant = etudiants.sample(1).iloc[0]
        now = datetime.utcnow()
        session = Session(
            id_session=f"sess_{len(sessions)+1:04d}",
            id_etudiant=int(etudiant["id"]),
            debut=now.isoformat(),
            fin=(now + timedelta(minutes=random.randint(30, 120))).isoformat(),
            id_salle=random.choice(salles)
        )
        sessions.append(session.dict())
        await asyncio.sleep(30)

async def start_background_task():
    asyncio.create_task(generate_sessions())

def get_sessions():
    return sessions
