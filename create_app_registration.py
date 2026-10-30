from typing import Any, Literal

from graph_client import GraphClient


SignInAudience = Literal[
    "AzureADMyOrg",
    "AzureADMultipleOrgs",
    "AzureADandPersonalMicrosoftAccount",
    "PersonalMicrosoftAccount",
]


def create_app_registration(
    graph: GraphClient,
    display_name: str,
    sign_in_audience: SignInAudience = "AzureADMyOrg",
) -> dict[str, Any]:
    return graph.request(
        "POST",
        "/applications",
        json={
            "displayName": display_name,
            "signInAudience": sign_in_audience,
        },
    )
