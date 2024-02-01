from lefdef_class import Component, Macro
from bookshelf_class import ObjectDB, Nets, Region


def make_macros_and_components_from_bookshelf(
    object_db: ObjectDB, nets: Nets
) -> tuple[list[Macro], list[Component]]:
    macro_dict: dict[str, Macro] = {}
    comp_list: list[Component] = []
    macro_idx = 0
    for node_name, node in object_db.nodes.items():
        """
        Unique objects in ObjectDB are made into Macro instances.
        It should be unique by the combination of:
        - size
        - fixed/movable
        - pin composition (direction & offset coordinates)
        """
        size_str = f"({node.dx},{node.dy})"
        if node.is_fixed:
            size_str += "f"
        else:
            size_str += "m"
        pins_str = "".join(
            [
                f"{nets.pin_dict[pin_name].io}({coord[0]},{coord[1]})"
                for coord, pin_name in nets.pin_coord_dict[node_name].items()
            ]
        )
        macro_dict_key = size_str + pins_str

        if macro_dict_key in macro_dict:
            macro_name = macro_dict[macro_dict_key].name
        else:
            macro_name = f"Mac_{macro_idx}"
            macro_dict[macro_dict_key] = Macro(macro_name, node.dx, node.dy)
            for coord, pin_name in nets.pin_coord_dict[node_name].items():
                macro_dict[macro_dict_key].pin_dict[coord] = pin_name
            macro_idx += 1

        if node.is_fixed:
            component = Component(node_name, macro_name, "FIXED")
            component.lx, component.ly = node.lx, node.ly
        else:
            component = Component(node_name, macro_name, "UNPLACED")
        comp_list.append(component)

    print(f"{macro_idx} macros from {len(comp_list)} components")
    return list(macro_dict.values()), comp_list


class PhysDesignData:
    region: Region
    macros: list[Macro]
    components: list[Component]
    nets: Nets
