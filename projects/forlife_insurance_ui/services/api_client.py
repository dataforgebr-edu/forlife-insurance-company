import os

import httpx
from dotenv import load_dotenv

load_dotenv()

_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


class ApiClient:
    def __init__(self):
        self._client = httpx.Client(base_url=_BASE_URL, timeout=10.0)

    # --- Domínios ---

    def get_estados(self) -> list[dict]:
        return self._client.get("/dominios/estados").json()

    def get_cidades(self, estado_id: int | None = None) -> list[dict]:
        params = {"estado_id": estado_id} if estado_id else {}
        return self._client.get("/dominios/cidades", params=params).json()

    def get_produtos(self) -> list[dict]:
        return self._client.get("/dominios/produtos").json()

    def get_status_apolice(self) -> list[dict]:
        return self._client.get("/dominios/status-apolice").json()

    def get_periodicidades(self) -> list[dict]:
        return self._client.get("/dominios/periodicidades").json()

    def get_meios_pagamento(self) -> list[dict]:
        return self._client.get("/dominios/meios-pagamento").json()

    def get_status_sinistro(self) -> list[dict]:
        return self._client.get("/dominios/status-sinistro").json()

    # --- Apólices ---

    def get_apolices(self, skip: int = 0, limit: int = 100) -> list[dict]:
        return self._client.get(
            "/apolices", params={"skip": skip, "limit": limit}
        ).json()

    def get_apolice(self, apolice_id: int) -> dict:
        return self._client.get(f"/apolices/{apolice_id}").json()

    def create_apolice(self, data: dict) -> dict:
        return self._client.post("/apolices", json=data).json()

    def update_apolice(self, apolice_id: int, data: dict) -> dict:
        return self._client.put(f"/apolices/{apolice_id}", json=data).json()

    # --- Clientes ---

    def get_clientes(self, skip: int = 0, limit: int = 100) -> list[dict]:
        return self._client.get(
            "/clientes", params={"skip": skip, "limit": limit}
        ).json()

    def get_cliente(self, cliente_id: int) -> dict:
        return self._client.get(f"/clientes/{cliente_id}").json()

    def create_cliente(self, data: dict) -> dict:
        return self._client.post("/clientes", json=data).json()

    def update_cliente(self, cliente_id: int, data: dict) -> dict:
        return self._client.put(f"/clientes/{cliente_id}", json=data).json()

    # --- Corretores ---

    def get_corretores(self, skip: int = 0, limit: int = 100) -> list[dict]:
        return self._client.get(
            "/corretores", params={"skip": skip, "limit": limit}
        ).json()

    def get_corretor(self, corretor_id: int) -> dict:
        return self._client.get(f"/corretores/{corretor_id}").json()

    def create_corretor(self, data: dict) -> dict:
        return self._client.post("/corretores", json=data).json()

    def update_corretor(self, corretor_id: int, data: dict) -> dict:
        return self._client.put(f"/corretores/{corretor_id}", json=data).json()

    # --- Sinistros ---

    def get_sinistros(
        self, skip: int = 0, limit: int = 100, apolice_id: int | None = None
    ) -> list[dict]:
        params: dict = {"skip": skip, "limit": limit}
        if apolice_id is not None:
            params["apolice_id"] = apolice_id
        return self._client.get("/sinistros", params=params).json()

    def get_sinistro(self, sinistro_id: int) -> dict:
        return self._client.get(f"/sinistros/{sinistro_id}").json()

    def create_sinistro(self, data: dict) -> dict:
        return self._client.post("/sinistros", json=data).json()

    def update_sinistro(self, sinistro_id: int, data: dict) -> dict:
        return self._client.put(f"/sinistros/{sinistro_id}", json=data).json()

    # --- Parcelas ---

    def get_parcelas(
        self, skip: int = 0, limit: int = 100, apolice_id: int | None = None
    ) -> list[dict]:
        params: dict = {"skip": skip, "limit": limit}
        if apolice_id is not None:
            params["apolice_id"] = apolice_id
        return self._client.get("/parcelas", params=params).json()

    def get_parcela(self, parcela_id: int) -> dict:
        return self._client.get(f"/parcelas/{parcela_id}").json()

    def create_parcela(self, data: dict) -> dict:
        return self._client.post("/parcelas", json=data).json()

    def update_parcela(self, parcela_id: int, data: dict) -> dict:
        return self._client.put(f"/parcelas/{parcela_id}", json=data).json()
