from fastapi import FastAPI
from routes import users, inventory, pvp, missions, items, brotherhood, pet, stable, blacksmith, alchemist, tavern, coliseum, story, xp_curve

app = FastAPI()

app.include_router(users.router)
app.include_router(inventory.router)
app.include_router(pvp.router)
app.include_router(missions.router)
app.include_router(items.router)
app.include_router(brotherhood.router)
app.include_router(pet.router)
app.include_router(stable.router)
app.include_router(blacksmith.router)
app.include_router(alchemist.router)
app.include_router(tavern.router)
app.include_router(coliseum.router)
app.include_router(story.router)
app.include_router(xp_curve.router)
# Puedes agregar aquí los routers para establo, herrero, alquimista, taberna, coliseo, etc. Ejemplo:
# from routes import stable, blacksmith, alchemist, tavern, coliseum
# app.include_router(stable.router)
# app.include_router(blacksmith.router)
# app.include_router(alchemist.router)
# app.include_router(tavern.router)
# app.include_router(coliseum.router)

@app.get("/")
def root():
    return {"msg": "Caminos de la Fe backend is running!"}
