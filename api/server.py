
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from api.routes import pets_router, mounts_router, weapons_router, nursery_router, player_router, community_router

app = FastAPI(title="Caminos de la Fe API")

# CORS para frontend local/testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pets_router)
app.include_router(mounts_router)
app.include_router(weapons_router)
app.include_router(nursery_router)
app.include_router(player_router)
app.include_router(community_router)

@app.get("/ping")
def ping():
    return {"status": "ok"}

@app.get("/factions/{player_level}")
def get_factions(player_level: int):
    base_factions = ["cruzados", "sarracenos", "antiguos"]
    advanced_factions = ["vikingos", "romanos", "egipcios"]
    if player_level >= 50:
        return {"factions": base_factions + advanced_factions}
    return {"factions": base_factions}

@app.get("/localization/{lang}")
def get_localization(lang: str):
    # TODO: Integrar con systems/lang_manager.py y archivos JSON
    return {"lang": lang, "strings": {}}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
