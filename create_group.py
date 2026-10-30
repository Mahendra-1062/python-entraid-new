from typing import Any, Literal

from graph_client import GraphClient


GroupType = Literal["security", "microsoft-365"]


def create_group(
    graph: GraphClient,
    display_name: str,
    mail_nickname: str,
    description: str = "",
    group_type: GroupType = "security",
) -> dict[str, Any]:
    is_microsoft_365 = group_type == "microsoft-365"
    return graph.request(
        "POST",
        "/groups",
        json={
            "displayName": display_name,
            "description": description,
            "mailEnabled": is_microsoft_365,
            "mailNickname": mail_nickname,
            "securityEnabled": not is_microsoft_365,
            "groupTypes": ["unified"] if is_microsoft_365 else [],
        },
    )

