#  Copyright (c) 2023. Stefan Eiermann
#  Licenced under AGPL see /LICENSE
"""
Defines parts


"""
import uuid


class Part:
    all_parts = []

    def __init__(self, name):
        """
        This defines a characteristic of Simulation

        :param name: Name of current Simulation characteristic
        :type name: str
        """
        self.name = name
        self.characteristics = {}
        self.parent_parts = {}
        self.child_parts = {}
        self.uuid = uuid.uuid4()
        self.__class__.all_parts.append(self)

    def __str__(self):
        """
        String representation of Part object
        """
        return f'<{self.__class__.__name__} name="{self.name}">'

    def __repr__(self):
        """
        Representation of Part object
        """
        return f'<{self.__class__.__name__} name="{self.name}">'

    def get_name(self):
        return self.name

    def has(self, name):
        return name in self.characteristics

    def get(self, name):
        return self.characteristics.get(name)

    def attach_characteristic(self, characteristic):
        """
        Attaches a direct Part Characteristic object
        The Difference to register_characteristic is that this method is only used to connect a Part Characteristic to it self
        register_characteristic is used to connect to Parts via a Characteristic together

        :param characteristic:
        :return:
        """
        self.characteristics[characteristic.get_name()] = characteristic

    def register_characteristic(self, characteristic, category_name="generic"):
        """
        Add a Characteristic to the Part object
        The Difference to attach_characteristic is that this method links a Characteristic from another Part to this Part
        attach_characteristic attaches a the Characteristick of this Part to it self

        :param characteristic: Characteristic wich want to add to the Part object
        :type characteristic: Instance of BaseCharacteristic
        :param category_name: Category wich should be used. Each Category is Unique. Default is "generic"
        :type category_name: str
        :return: Current Part
        """

        if characteristic.get_name() not in self.child_parts:
            self.child_parts[characteristic.get_name()] = {}

        if category_name not in self.child_parts[characteristic.get_name()]:
            self.child_parts[characteristic.get_name()][category_name] = set({})
        self.child_parts[characteristic.get_name()][category_name].add(
            characteristic.part
        )
        return self

    def goto_parent(self, component_type, category_name):
        parent_cmp = self.parent_parts.get(component_type, {}).get(category_name, None)
        if parent_cmp is not None:
            return parent_cmp.goto_parent(component_type, category_name)
        return self

    def filtered_tree(
        self,
        component_type,
        category_name="generic",
        use_global=False,
        add_parent=False,
        **kwargs,
    ):
        if use_global:
            result_list = []

            for cmp in self.__class__.all_parts:
                parent_cmp = cmp.goto_parent(component_type, category_name)
                item = parent_cmp.filtered_tree(
                    component_type,
                    category_name=category_name,
                    use_global=False,
                    add_parent=add_parent,
                )
                if len(item.get("children")) > 0:
                    if (
                        len(
                            list(
                                filter(
                                    lambda x: x.get("name") == item.get("name"),
                                    result_list,
                                )
                            )
                        )
                        <= 0
                    ):
                        result_list.append(item)
            return result_list
        else:
            components = self.child_parts.get(component_type, {}).get(
                category_name, set({})
            )
            if category_name == "generic":
                components = []
                for key, catlist in self.child_parts.get(component_type, {}).items():
                    components = components + list(catlist)

            current_element = {"name": self.name, "children": [], "part": self}
            for child in components:
                current_element["children"].append(
                    child.filtered_tree(
                        component_type, category_name, use_global=use_global
                    )
                )
            return current_element

    @classmethod
    def filter(cls, component_type, category_name):
        result_list = []
        for cmp in cls.all_parts:
            if (
                len(cmp.child_parts.get(component_type, {}).get(category_name, set({})))
                > 0
            ):
                result_list.append(cmp)
        return result_list

    def get_values(self, component_type, category_name, children_also):
        cols = ["name"]

        results = []
        subcomponent = self.get(component_type)

        cols, subvalues = subcomponent.get_values()

        results.append(subvalues)

        if children_also:
            components = self.child_parts.get(component_type, {}).get(
                category_name, set({})
            )
            for cmp in components:
                cmpcol, cmpvalue = cmp.get_values(
                    component_type, category_name, children_also=children_also
                )
                results = results + cmpvalue

        return list(cols), results

    def is_connected(
        self, target_component, component_type, category_name, parent_search=True
    ):
        parent_component = self
        if parent_search:
            parent_component = self.goto_parent(component_type, category_name)

        for child_cmp in parent_component.child_parts.get(component_type, {}).get(
            category_name, set({})
        ):
            if child_cmp is target_component:
                return True
            if child_cmp.is_connected(
                target_component, component_type, category_name, parent_search=False
            ):
                return True
        return False
