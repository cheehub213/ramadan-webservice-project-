#!/usr/bin/env python3
"""Direct FastAPI app test"""

import sys
sys.path.insert(0, '.')

from fastapi import FastAPI
from app.routes import imam
from app.database import Base, engine

app = FastAPI()
app.include_router(imam.router)

# Create tables
Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    import uvicorn
    print("Starting server...")
    uvicorn.run(app, host="127.0.0.1", port=8002)
