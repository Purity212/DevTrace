from __future__ import annotations

from io import BytesIO
from typing import Any

import requests


DEFAULT_API_BASE = "http://127.0.0.1:8000"
DEFAULT_TIMEOUT = 30


def get_api_base() -> str:
    import streamlit as st

    return st.session_state.get("api_base", DEFAULT_API_BASE).rstrip("/")


def extract_error_message(response: requests.Response) -> str:
    try:
        payload = response.json()
    except ValueError:
        return response.text or f"HTTP {response.status_code}"

    if isinstance(payload, dict) and "detail" in payload:
        return str(payload["detail"])
    return str(payload)


def check_health() -> dict[str, Any]:
    response = requests.get(f"{get_api_base()}/health", timeout=10)
    response.raise_for_status()
    return response.json()


def get_projects() -> list[dict[str, Any]]:
    response = requests.get(f"{get_api_base()}/projects", timeout=10)
    response.raise_for_status()
    return response.json()


def create_project(name: str, description: str | None) -> dict[str, Any]:
    payload = {"name": name, "description": description}
    response = requests.post(f"{get_api_base()}/projects", json=payload, timeout=10)
    response.raise_for_status()
    return response.json()


def get_documents(project_id: int) -> list[dict[str, Any]]:
    response = requests.get(
        f"{get_api_base()}/projects/{project_id}/documents",
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def upload_document(project_id: int, document_type: str, uploaded_file: Any) -> dict[str, Any]:
    files = {
        "file": (
            uploaded_file.name,
            BytesIO(uploaded_file.getvalue()),
            uploaded_file.type or "text/plain",
        )
    }
    data = {"document_type": document_type}

    response = requests.post(
        f"{get_api_base()}/projects/{project_id}/documents",
        files=files,
        data=data,
        timeout=DEFAULT_TIMEOUT,
    )
    response.raise_for_status()
    return response.json()


def run_analysis(project_id: int) -> dict[str, Any]:
    response = requests.post(
        f"{get_api_base()}/projects/{project_id}/analyze",
        timeout=DEFAULT_TIMEOUT,
    )
    response.raise_for_status()
    return response.json()
