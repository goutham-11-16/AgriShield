import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from backend.app.core.config import settings
from backend.app.api import predict, protect, recover, reconnect, sync

app = FastAPI(
    title=settings.APP_NAME,
    description="AgriShield: AI-Powered Farmer Decision, Crop Protection & Recovery Platform for Indian Agriculture",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for Web Dashboard & Android clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API Routers
app.include_router(predict.router, prefix=settings.API_V1_STR)
app.include_router(protect.router, prefix=settings.API_V1_STR)
app.include_router(recover.router, prefix=settings.API_V1_STR)
app.include_router(reconnect.router, prefix=settings.API_V1_STR)
app.include_router(sync.router, prefix=settings.API_V1_STR)

# Find web dashboard dist directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
web_dist_path = os.path.join(BASE_DIR, "web-dashboard", "dist")

if os.path.exists(web_dist_path) and os.path.exists(os.path.join(web_dist_path, "assets")):
    app.mount("/assets", StaticFiles(directory=os.path.join(web_dist_path, "assets")), name="assets")

@app.get("/")
async def root(request: Request):
    # If client accepts HTML and index.html exists, serve the dashboard
    accept_header = request.headers.get("accept", "")
    index_html = os.path.join(web_dist_path, "index.html")
    if "text/html" in accept_header and os.path.exists(index_html):
        return FileResponse(index_html)
    
    return {
        "platform": settings.APP_NAME,
        "tagline": "Predict, Protect & Recover",
        "pilot_region": settings.PILOT_STATE,
        "status": "operational",
        "documentation": "/docs"
    }

@app.get("/dashboard")
async def dashboard():
    index_html = os.path.join(web_dist_path, "index.html")
    if os.path.exists(index_html):
        return FileResponse(index_html)
    return {"message": "Web dashboard dist build not found. Run 'npm run build' inside web-dashboard/"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "database": "connected"
    }
