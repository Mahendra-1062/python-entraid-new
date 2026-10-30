from typing import Any

from graph_client import GraphClient, normalize_object_id


def create_enterprise_app(graph: GraphClient, app_id: str) -> dict[str, Any]:
    app_id = normalize_object_id(app_id)
    matches = graph.request(
        "GET",
        "/servicePrincipals",
        params={
            "$filter": f"appId eq '{app_id}'",
            "$select": "id,appId,displayName",
        },
    )
    if matches["value"]:
        return matches["value"][0]

    return graph.request(
        "POST", "/servicePrincipals", json={"appId": app_id}
    )
