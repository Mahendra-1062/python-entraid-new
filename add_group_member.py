from graph_client import GRAPH_BASE_URL, GraphClient, normalize_object_id


def add_group_member(
    graph: GraphClient, group_id: str, member_id: str
) -> None:
    group_id = normalize_object_id(group_id)
    member_id = normalize_object_id(member_id)
    graph.request(
        "POST",
        f"/groups/{group_id}/members/$ref",
        json={"@odata.id": f"{GRAPH_BASE_URL}/directoryObjects/{member_id}"},
    )
