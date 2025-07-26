from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import List

from .database import engine, Base
from .routers import conversation, chat
from .auth import get_current_active_user

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="E-Commerce Chat API")

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(conversation.router)
app.include_router(chat.router)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Protected test endpoint
@app.get("/protected-route")
async def protected_route(current_user=Depends(get_current_active_user)):
    return {"message": f"Hello {current_user.email}"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
