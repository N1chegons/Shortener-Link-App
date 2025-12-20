from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware



app = FastAPI(
    title="Link Shortener",
    summary="In this project, you can shorten links using this API."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "PUT", "PATCH", "DELETE"],
    allow_headers=["*"],
)

@app.get("/")
async def get_home_page():
    return {
        "status": 200,
        "message": "Hello"
    }

from src.auth.router import router as auth_router
from src.link.router import router

app.include_router(router)
app.include_router(auth_router)