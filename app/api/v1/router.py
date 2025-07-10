from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.endpoints import user
from app.api.v1.endpoints import report

app = FastAPI()
# Development CORS settings — allow everything (localhost testing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict to ["http://localhost:3000"] in real dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
api_router = APIRouter()
api_router.include_router(user.router, prefix="/api/v1/user", tags=["user"])
api_router.include_router(report.router, prefix="/api/v1/report", tags=["report and tips"])
app.include_router(api_router)
