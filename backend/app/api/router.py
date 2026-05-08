from fastapi import APIRouter

from app.api.novels import router as novels_router
from app.api.download import router as download_router
from app.api.export import router as export_router
from app.api.rules import router as rules_router
from app.api.search import router as search_router
from app.api.settings import router as settings_router

api_router = APIRouter()

api_router.include_router(novels_router, prefix="/novels", tags=["novels"])
api_router.include_router(download_router, prefix="/download", tags=["download"])
api_router.include_router(export_router, prefix="/export", tags=["export"])
api_router.include_router(rules_router, prefix="/rules", tags=["rules"])
api_router.include_router(search_router, prefix="/search", tags=["search"])
api_router.include_router(settings_router, prefix="/settings", tags=["settings"])
