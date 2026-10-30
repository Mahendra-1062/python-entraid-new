import re
from typing import Any

from graph_client import GraphClient
from create_group import create_group


def create_user(
    graph: GraphClient,
    display_name: str,
    user_principal_name: str,
    password: str,
    mail_nickname: str | None = None,
) -> dict[str, Any]:
    if not password:
        raise ValueError("Password must not be empty.")

    nickname = mail_nickname or re.sub(
        r"[^A-Za-z0-9._'-]", "", user_principal_name.split("@", 1)[0]
    )
    if not nickname:
        raise ValueError("Could not derive a mail nickname; provide one explicitly.")

    description="Manage Microsoft Entra ID objects through Microsoft Graph."
    group_type = "security"
    result = create_group(
    graph,
    display_name,
    mail_nickname,
    description,
    group_type,
)
    return graph.request(
        "POST",
        "/users",
        json={
            "accountEnabled": True,
            "displayName": display_name,
            "mailNickname": nickname,
            "userPrincipalName": user_principal_name,
            "passwordProfile": {
                "forceChangePasswordNextSignIn": True,
                "password": password,
            },
        },
    )
