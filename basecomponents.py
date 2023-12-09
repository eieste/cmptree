import enum
import pandas as pd
import uuid


class ElectricSignal(enum.Enum):
    name = "electric"

    POWER_IN = "PWR_IN"
    POWER_LVL_5 = "PWR_LVL_5"
    POWER_LVL_7 = "PWR_LVL_7"
    I2C = "I2C"
    PWMCTL = "PWM-CTL"
    PWMFEED = "PWM-FEED"
    PICAM = "PICAM"
    PIDISPLAY = "PIDISPLAY"
    USB = "USB"
    SERIAL = "SERIAL"
    OTHER = "OTHER"


class Component:
    all_components = []

    def __init__(self, name, todo=False):
        self.name = name
        self.todo = todo
        self.sub_components = {}
        self.parent_components = {}
        self.children_components = {}
        self.uuid = uuid.uuid4()
        self.__class__.all_components.append(self)

    def __str__(self):
        return f"<{self.__class__.__name__} name=\"{self.name}\">"

    def __repr__(self):
        return f"<{self.__class__.__name__} name=\"{self.name}\">"

    def get_name(self):
        return self.name

    def has(self, name):
        return name in self.sub_components

    def get(self, name):
        return self.sub_components.get(name)

    def attach_subcomponent(self, sub_component):
        self.sub_components[sub_component.get_name()] = sub_component

    def register_children(self, subcomponent, category_name="generic"):
        if subcomponent.get_name() not in self.children_components:
            self.children_components[subcomponent.get_name()] = {}

        if category_name not in self.children_components[subcomponent.get_name()]:
            self.children_components[subcomponent.get_name()][category_name] = set({})
        self.children_components[subcomponent.get_name()][category_name].add(subcomponent.component)
        return self

    def goto_parent(self, component_type, category_name):
        parent_cmp = self.parent_components.get(component_type, {}).get(category_name, None)
        if parent_cmp is not None:
            return parent_cmp.goto_parent(component_type, category_name)
        return self

    def filtered_tree(self, component_type, category_name="generic", use_global=False, add_parent=False, **kwargs):
        if use_global: 
            result_list = []

            for cmp in self.__class__.all_components:
                parent_cmp = cmp.goto_parent(component_type, category_name)
                item = parent_cmp.filtered_tree(component_type, category_name=category_name, use_global=False, add_parent=add_parent)
                if len(item.get("children")) > 0:
                    if len(list(filter(lambda x: x.get("name") == item.get("name"), result_list))) <= 0:
                        result_list.append(item)
            return result_list
        else:
            components = self.children_components.get(component_type, {}).get(category_name, set({}))
            if category_name == "generic":
                components = []
                for key, catlist in self.children_components.get(component_type, {}).items():
                    components = components + list(catlist)

            current_element = {
                "name": self.name,
                "children": [],
                "component": self
            }
            for child in components:
                current_element["children"].append(
                    child.filtered_tree(component_type, category_name, use_global=use_global)
                )
            return current_element

    @classmethod
    def filter(cls, component_type, category_name):
        result_list = []
        for cmp in cls:
            if len(cmp.children_components.get(component_type, {}).get(category_name, set({}))) > 0:
                result_list.append(cmp)
        return result_list

    def get_values(self, component_type, category_name, children_also):
        cols = ["name"]

        results = [
            
        ]
        subcomponent = self.get(component_type)

        cols, subvalues = subcomponent.get_values()

        results.append(subvalues) 
        
        if children_also:
            components = self.children_components.get(component_type, {}).get(category_name, set({}))
            for cmp in components:
                cmpcol, cmpvalue = cmp.get_values(component_type, category_name, children_also=children_also)
                results = results + cmpvalue
                       
        return list(cols), results

    def print(self, component_type, category_name, children_also=False):
        cols, result = self.get_values(component_type, category_name, children_also=children_also)
        print(result)
        df = pd.DataFrame(result, columns=cols)
        df.style.hide(axis="index")
        return df        
    
    def is_connected(self, target_component, component_type, category_name, parent_search=True):
        parent_component = self
        if parent_search:
            parent_component = self.goto_parent(component_type, category_name)

        for child_cmp in parent_component.children_components.get(component_type, {}).get(category_name, set({})):
            if child_cmp is target_component:
                return True
            if child_cmp.is_connected(target_component, component_type, category_name, parent_search=False):
                return True

        return False


        

class BaseSubComponent:

    def __init__(self, component, **kwargs):
        self.component = component
        if self.get_name() in component.sub_components:
            raise ValueError(f"{self.get_name()} already attached")
        component.attach_subcomponent(self)

    def __str__(self):
        return f"<{self.__class__.__name__} component=\"{self.component.name}\">"

    def __repr__(self):
        return f"<{self.__class__.__name__} component=\"{self.component.name}\">"

    def get_name(self):
        if not hasattr(self, "name"):
            raise ValueError("Name is missing")
        return self.name

    def add_child(self, component):
        self.children_links.add(component)

    def set_parent(self, parent_component, category_name="generic"):

        if not isinstance(parent_component, Component):
            raise ValueError("Given value isnt a Component")

        if parent_component is self.component:
            raise ValueError("parent_component cant be my component")

        if category_name in self.component.parent_components.get(self.get_name(), {}):
            raise ValueError(f"My parent Component has already defined a parent component for {self.get_name()}")

        # Add Parent Component
        self.component.parent_components[self.get_name()] = {
            category_name: parent_component
        }

        # Add Children Component
        parent_component.register_children(self, category_name)
        return self

    def link_to_component(self, component):
        if not isinstance(component, Component):
            raise ValueError("Given value isnt a SubComponent")

        if self.parent_link is not None:
            raise ValueError("Parent Link already assigned")
        self.parent_link = component
        component.sub_components[self.get_name()].add_child(
            self.parent_component)

    def filterd_tree(self, component_type, category_name, use_global=False, parent_node=None):
        x = parent_node.find(self.component.parent_components.get(component_type, {}).get(category_name))

        if self.get_name() == component_type:
            new_node = Node(self.component)
            parent_node.add_child(new_node)
            self.component.filterd_tree(component_type, category_name, use_global=use_global, parent_node=new_node)

    def get_values(self):
        cols, values = set({"Name"}), []

        values.append(self.component.name)
        
        for key, unit in self.units.items():
            cols.add(key)
            values.append(str(getattr(self, key))+" "+unit)
        return cols, values


class ThermalComponent(BaseSubComponent):
    name = "thermal"

    def __init__(self, *args, btu=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.btu = btu
        self.units = {
            "btu": "btu"
        }


class MechanicComponent(BaseSubComponent):
    name = "mechanic"

    def __init__(self, *args, torque=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.torque = torque
        self.units = {
            "torque": "Nm"
        }


class ElectricSupplyComponent(BaseSubComponent):
    name = "electric"

    def __init__(self, *args, capacity=None, c_value=None, nominal_voltage=None,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.capacity = capacity
        self.c_value = c_value
        self.nominal_voltage = nominal_voltage
        self.units = {
            "capacity": "A/h",
            "c_value": "c",
            "nominal_voltage": "V"
        }


class ElectricConvertComponent(BaseSubComponent):
    name = "electric"

    def __init__(self, *args, maximal_in_voltage=None,
                 maximal_in_current=None,
                 nominal_out_voltage=None,
                 nominal_out_current=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.maximal_in_voltage = maximal_in_voltage
        self.maximal_in_current = maximal_in_current
        self.nominal_out_voltage = nominal_out_voltage
        self.nominal_out_current = nominal_out_current
        self.units = {
            "maximal_in_voltage": "V",
            "maximal_in_current": "A",
            "nominal_out_voltage": "V",
            "nominal_out_current": "A"
        }


class ElectricDistributorComponent(BaseSubComponent):
    name = "electric"

    def __init__(self, *args, bus=None, distribution_voltage=None,
                 signal_name=None,
                 maximal_current=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.distribution_voltage = distribution_voltage
        self.maximal_current = maximal_current
        self.bus = bus
        self.units = {
            "distribution_voltage": "V",
            "maximal_current": "A"
        }

class ElectricComponent(BaseSubComponent):
    name = "electric"

    def __init__(self, *args, required_voltage=None, required_current=None,
                 maximal_current=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.nominal_voltage = required_voltage
        self.nominal_current = required_current
        self.maximal_current = maximal_current
        self.units = {
            "nominal_voltage": "V",
            "nominal_current": "A",
            "maximal_current": "A"
        }


class DimensionComponent(BaseSubComponent):
    name = "dimension"

    def __init__(self, *args, weight=None, height=None, width=None, length=None,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.weight = weight
        self.height = height
        self.width = width
        self.length = length
        self.units = {
            "weight": "g",
            "height": "mm",
            "width": "mm",
            "length": "mm"
        }