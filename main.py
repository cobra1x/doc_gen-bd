from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
from app.api import tools_routes
from contextlib import asynccontextmanager # <-- Import this

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- DEFINE THE LIFESPAN EVENT HANDLER ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handle application startup and shutdown events.
    This replaces the deprecated on_event("shutdown").
    """
    logging.info("DocGen Tools Service startup...")
    
    yield # This is where the application will run
    
    # This code runs on shutdown
    logging.info("DocGen Tools Service shutdown.")
# -----------------------------------------

app = FastAPI(
    title="DocGen Tools Service",
    description="API for generating legal documents (PDF, DOCX).",
    version="1.0.0",
    lifespan=lifespan # <-- Assign the lifespan handler here
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- The @app.on_event("shutdown") function has been removed ---
# --- and replaced by the lifespan manager above. ---

# Include only the tools_routes router
app.include_router(tools_routes.router)

@app.get("/")
def root():
    return {
        "message": "DocGen Tools Service is running.",
        "docs": "/docs"
    }

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logging.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred."}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8003, reload=True)

