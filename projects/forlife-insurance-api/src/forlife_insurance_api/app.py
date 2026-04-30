from __future__ import annotations

from fastapi import FastAPI
from forlife_insurance_api.routers.apolice import router

app = FastAPI(
    title="ForLife Insurance API",
    version="0.1.0",
    description="API transacional para consumo do domínio de seguros.",
)

app.include_router(router)
