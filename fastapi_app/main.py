from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_app.database import engine, Base
from fastapi_app.endpoints import reports, search

app = FastAPI(title="Telegram Data Product API")

# Create tables if not exist
Base.metadata.create_all(bind=engine)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(reports.router, prefix="/reports", tags=["reports"])
app.include_router(search.router, prefix="/search", tags=["search"])

@app.get("/")
def root():
    return {"message": "Welcome to Telegram Data Product API"}
