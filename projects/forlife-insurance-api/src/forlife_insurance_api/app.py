from __future__ import annotations

from fastapi import FastAPI
from forlife_insurance_api.routers.apolice import router as apolice_router
from forlife_insurance_api.routers.cliente import router as cliente_router
from forlife_insurance_api.routers.corretor import router as corretor_router
from forlife_insurance_api.routers.dominios import router as dominios_router
from forlife_insurance_api.routers.parcela import router as parcela_router
from forlife_insurance_api.routers.sinistro import router as sinistro_router

app = FastAPI(
    title="ForLife Insurance API",
    version="0.1.0",
    description="API transacional para consumo do domínio de seguros.",
)

app.include_router(apolice_router)
app.include_router(cliente_router)
app.include_router(corretor_router)
app.include_router(parcela_router)
app.include_router(sinistro_router)
app.include_router(dominios_router)
