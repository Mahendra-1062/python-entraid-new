import os
from typing import Any
from uuid import UUID

import msal
import requests


GRAPH_BASE_URL = "https://graph.microsoft.com/v1.0"
GRAPH_SCOPE = ["https://graph.microsoft.com/.default"]


def normalize_object_id(value: str) -> str:
    try:
        return str(UUID(value))
    except ValueError as error:
        raise ValueError(f"{value!r} must be a valid GUID.") from error


class GraphAPIError(RuntimeError):
    def __init__(self, status_code: int, response_text: str) -> None:
        super().__init__(f"Microsoft Graph returned HTTP {status_code}: {response_text}")
        self.status_code = status_code
        self.response_text = response_text


class GraphClient:
    def __init__(self) -> None:
        required = ("ENTRA_TENANT_ID", "ENTRA_CLIENT_ID", "ENTRA_CLIENT_SECRET")
        missing = [name for name in required if not os.environ.get(name)]
        if missing:
            raise RuntimeError(
                "Missing required environment variables: " + ", ".join(missing)
            )

        tenant_id = os.environ["ENTRA_TENANT_ID"]
        application = msal.ConfidentialClientApplication(
            client_id=os.environ["ENTRA_CLIENT_ID"],
            authority=f"https://login.microsoftonline.com/{tenant_id}",
            client_credential=os.environ["ENTRA_CLIENT_SECRET"],
        )
        token_result = application.acquire_token_for_client(scopes=GRAPH_SCOPE)
        access_token = token_result.get("access_token")
        if not access_token:
            detail = token_result.get("error_description", "No access token was returned.")
            raise RuntimeError(f"Microsoft identity platform authentication failed: {detail}")

        self._headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

    def request(
        self,
        method: str,
        path_or_url: str,
        *,
        json: dict[str, Any] | None = None,
        params: dict[str, str] | None = None,
    ) -> Any:
        url = (
            path_or_url
            if path_or_url.startswith("https://")
            else f"{GRAPH_BASE_URL}/{path_or_url.lstrip('/')}"
        )
        response = requests.request(
            method,
            url,
            headers=self._headers,
            json=json,
            params=params,
            timeout=30,
        )
        if not response.ok:
            raise GraphAPIError(response.status_code, response.text)
        if response.status_code == 204 or not response.content:
            return None
        return response.json()
