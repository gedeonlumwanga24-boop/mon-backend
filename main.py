from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal, Message, create_db

app = FastAPI()

# Autoriser toutes les origines (cors)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modèle pour les contacts
class Contact(BaseModel):
    nom: str
    email: str
    message: str

# Créer la DB au démarrage
@app.on_event("startup")
def startup():
    create_db()

# Route d'accueil
@app.get("/")
def home():
    return {"message": "Bienvenue sur mon backend !"}

# Endpoint pour recevoir un message
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

# Endpoint pour lister tous les messages
@app.get("/messages")
def lister_messages():
    db = SessionLocal()
    messages = db.query(Message).all()
    db.close()
    return {"messages": [{"nom": m.nom, "email": m.email, "message": m.message} for m in messages]}
