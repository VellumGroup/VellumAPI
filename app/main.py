from fastapi import FastAPI
from auth.router import router as auth_router
from billing.router import router as billing_router
from notes.router import router as notes_router
from notes.realtime import router as ws_router
from users.router import router as users_router
# TODO: MAKE THE DAMN FILE IMPORTS WORK BECAUSE I DONT KNOW HOW

app = FastAPI()

app.include_router(auth_router)
app.include_router(billing_router)
app.include_router(notes_router)
app.include_router(ws_router)
app.include_router(users_router)

@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "1.0.0"}

@app.get("/stats")
def system_stats():
    return {"status": "operational", "uptime": "99.9%"}