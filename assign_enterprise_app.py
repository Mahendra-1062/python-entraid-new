from typing import Any

from graph_client import GraphClient, normalize_object_id


DEFAULT_ACCESS_ROLE_ID = "00000000-0000-0000-0000-000000000000"


def assign_enterprise_app(
    graph: GraphClient,
    service_principal_id: str,
    principal_id: str,
    app_role_id: str = DEFAULT_ACCESS_ROLE_ID,
) -> dict[str, Any]:
    service_principal_id = normalize_object_id(service_principal_id)
    principal_id = normalize_object_id(principal_id)
    app_role_id = normalize_object_id(app_role_id)

    return graph.request(
        "POST",
        f"/servicePrincipals/{service_principal_id}/appRoleAssignedTo",
        json={
            "principalId": principal_id,
            "resourceId": service_principal_id,
            "appRoleId": app_role_id,
        },
    )
