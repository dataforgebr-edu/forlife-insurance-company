from __future__ import annotations

from fastapi import FastAPI
from forlife_insurance_extract.routers.apolice import router

app = FastAPI(
    title="ForLife Insurance Extract API",
    version="0.1.0",
    description="Endpoints de extração para consumo analítico e data lake.",
)

app.include_router(router)
