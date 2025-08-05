from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Caminos de la Fe API")

# CORS para frontend local/testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ping")
def ping():
    return {"status": "ok"}

# Endpoint de perfil de jugador
@app.get("/profile/{player_id}")
def get_profile(player_id: str):
    # TODO: Integrar con sistema de jugadores
    return {"player_id": player_id, "stats": {}, "faction": None}

# Endpoint de facciones

# Endpoint de facciones avanzadas según nivel
@app.get("/factions/{player_level}")
def get_factions(player_level: int):
    base_factions = ["cruzados", "sarracenos", "antiguos"]
    advanced_factions = ["vikingos", "romanos", "egipcios"]
    if player_level >= 50:
        return {"factions": base_factions + advanced_factions}
    return {"factions": base_factions}

# Endpoint de localización
@app.get("/localization/{lang}")
def get_localization(lang: str):
    # TODO: Integrar con systems/lang_manager.py y archivos JSON
    return {"lang": lang, "strings": {}}

# Puedes agregar más endpoints aquí

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
