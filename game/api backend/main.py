from fastapi import FastAPI
from routes import users, inventory, pvp, missions, items, clan

app = FastAPI()

app.include_router(users.router)
app.include_router(inventory.router)
app.include_router(pvp.router)
app.include_router(missions.router)
app.include_router(items.router)
app.include_router(clan.router)

@app.get("/")
def root():
    return {"msg": "Caminos de la Fe backend is running!"}
