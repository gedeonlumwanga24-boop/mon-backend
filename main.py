from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal, Message, create_db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Contact(BaseModel):
    nom: str
    email: str
    message: str

# Créer la DB au démarrage
@app.on_event("startup")
def startup():
    create_db()

@app.post("/contact")
def recevoir_message(contact: Contact):
    db = SessionLocal()
    nouveau_message = Message(
        nom=contact.nom,
        email=contact.email,
        message=contact.message
    )
    db.add(nouveau_message)
    db.commit()
    db.close()

    return {"status": "success", "message": "Message enregistré 💾"}