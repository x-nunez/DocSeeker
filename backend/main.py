from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.sherlock.sherlock import router as search_router
from src.cloud.googleDrive import router as cloud_router

app = FastAPI()

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(cloud_router, tags=["cloud"])
app.include_router(search_router, prefix="/sherlock", tags=["sherlock"])