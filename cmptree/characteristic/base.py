#  Copyright (c) 2023. Stefan Eiermann
#  Licenced under AGPL see /LICENSE
from cmptree.part import Part


class BaseCharacteristic:
    def __init__(self, component, **kwargs):
        self.component = component
        if self.get_name() in component.characteristics:
            raise ValueError(f"{self.get_name()} already attached")
        component.attach_characteristic(self)

    def __str__(self):
        return f'<{self.__class__.__name__} part="{self.component.name}">'

    def __repr__(self):
        return f'<{self.__class__.__name__} part="{self.component.name}">'

    def get_name(self):
        if not hasattr(self, "name"):
            raise ValueError("Name is missing")
        return self.name

    def add_child(self, component):
        self.children_links.add(component)

    def set_parent(self, parent_part, category_name="generic"):

        if not isinstance(parent_part, Part):
            raise ValueError("Given value isnt a Component")

        if parent_part is self.component:
            raise ValueError("parent_part cant be my part")

        if category_name in self.component.parent_parts.get(self.get_name(), {}):
            raise ValueError(
                f"My parent Component has already defined a parent part for {self.get_name()}"
            )

        # Add Parent Component
        self.component.parent_parts[self.get_name()] = {category_name: parent_part}

        # Add Children Component
        parent_part.register_characteristic(self, category_name)
        return self

    def link_to_component(self, part):
        if not isinstance(part, Part):
            raise ValueError("Given value isnt a SubComponent")

        if self.parent_link is not None:
            raise ValueError("Parent Link already assigned")
        self.parent_link = part
        part.characteristics[self.get_name()].add_child(self.parent_component)

    def filterd_tree(
        self, component_type, category_name, use_global=False, parent_node=None
    ):
        x = parent_node.find(
            self.component.parent_parts.get(component_type, {}).get(category_name)
        )

        if self.get_name() == component_type:
            new_node = Node(self.component)
            parent_node.add_child(new_node)
            self.component.filterd_tree(
                component_type,
                category_name,
                use_global=use_global,
                parent_node=new_node,
            )

    def get_values(self):
        cols, values = set({"Name"}), []

        values.append(self.component.name)

        for key, unit in self.units.items():
            cols.add(key)
            values.append(str(getattr(self, key)) + " " + unit)
        return cols, values
