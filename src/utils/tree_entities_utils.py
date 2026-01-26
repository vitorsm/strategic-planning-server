from typing import List, Any, Dict


def build_tree(entities: List[dict], parent_parameter: str, id_parameter: str = "id") -> List[dict]:
    nodes_by_id: Dict[str, dict] = {}

    for entity in entities:
        entity["children"] = []
        nodes_by_id[entity[id_parameter]] = entity

    root_dtos = [dto for dto in nodes_by_id.values() if not dto[parent_parameter]]

    roots: List[dict] = []
    for entity in entities:
        parent_id = entity[parent_parameter][id_parameter] if entity[parent_parameter] else None
        parent_node = nodes_by_id.get(parent_id) if parent_id else None

        if parent_node:
            parent_node["children"].append(entity)
        else:
            roots.append(entity)

    return root_dtos