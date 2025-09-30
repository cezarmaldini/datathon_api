from config.settings import Settings
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from routers.vaga_routers import router as vaga_router
from routers.search import router as search_router
from routers.llm import router as llm_router
import logging
import traceback

# 🔧 CONFIGURAÇÃO DE LOGGING
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_settings():
    return Settings()

def create_application():
    settings = get_settings()

    app = FastAPI(
        title=settings.api_title,
        description=settings.api_description,
        version=settings.api_version
    )

    # 🔧 MIDDLEWARE GLOBAL DE TRATAMENTO DE ERROS
    @app.middleware("http")
    async def global_error_handler(request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            # Log completo do erro
            logger.error(f"🚨 ERRO GLOBAL NA API: {str(e)}")
            logger.error(f"📋 Stack trace: {traceback.format_exc()}")
            logger.error(f"🌐 Endpoint: {request.url}")
            logger.error(f"🔧 Method: {request.method}")
            
            # Retorna erro 500 sem crashar a aplicação
            return JSONResponse(
                status_code=500,
                content={
                    "detail": "Erro interno do servidor",
                    "error": str(e),
                    "type": type(e).__name__
                }
            )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
            "http://127.0.0.1:3000",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add routers
    app.include_router(vaga_router)
    app.include_router(search_router)
    app.include_router(llm_router)
    
    # 🔧 HEALTH CHECK SIMPLES
    @app.get("/")
    async def health_check():
        return {
            "status": "healthy",
            "service": settings.api_title,
            "version": settings.api_version
        }
    
    # 🔧 HEALTH CHECK DETALHADO
    @app.get("/health")
    async def detailed_health_check():
        try:
            # Testa se as configurações carregaram
            settings = get_settings()
            return {
                "status": "healthy",
                "api_title": settings.api_title,
                "qdrant_url": bool(settings.qdrant_url),
                "openai_key": bool(settings.openai_api_key),
                "postgres_configured": bool(settings.postgres_host)
            }
        except Exception as e:
            logger.error(f"❌ Health check failed: {str(e)}")
            raise HTTPException(500, f"Health check failed: {str(e)}")
    
    return app

app = create_application()