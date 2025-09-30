from config.settings import Settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.vaga_routers import router as vaga_router
from routers.search import router as search_router
from routers.llm import router as llm_router

def get_settings():
    return Settings()

def create_application():
    settings = get_settings()

    app = FastAPI(
        title=settings.api_title,
        description=settings.api_description,
        version=settings.api_version
    )

    app.add_middleware(
            CORSMiddleware,
            allow_origins=[
                "http://localhost:3000",
                "http://127.0.0.1:3000",
            ],  # Frontend local
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # Add routers
    app.include_router(vaga_router)
    app.include_router(search_router)
    app.include_router(llm_router)
    
    return app

app = create_application()