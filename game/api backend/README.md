# Caminos de la Fe Backend

This is the FastAPI + PostgreSQL backend for Caminos de la Fe: Cruzada y Conquista.

## Features
- User registration and authentication (JWT)
- Inventory and equipment management
- PvP duels and cooldowns
- Mission and quest progress
- Item trading and purification
- Clan and faction management
- Economy and gold transactions

## Tech Stack
- FastAPI (Python)
- PostgreSQL (SQLAlchemy ORM)
- JWT authentication
- Pydantic models

## Getting Started
1. Create a PostgreSQL database and set credentials in `.env`
2. Activate the Python virtual environment:
   ```powershell
   venv\Scripts\activate
   ```
3. Run the server:
   ```powershell
   uvicorn main:app --reload
   ```

## Folder Structure
- `main.py`: FastAPI app entry point
- `models/`: SQLAlchemy models
- `schemas/`: Pydantic schemas
- `routes/`: API endpoints
- `core/`: Auth, config, and utilities
- `.github/copilot-instructions.md`: Copilot custom instructions

## Example Endpoints
- `/register` - Create user
- `/login` - Get JWT token
- `/inventory` - Get/update inventory
- `/pvp/duel` - Start/resolve duel
- `/missions` - Get/update mission progress
- `/clan` - Clan management

## License
MIT
