class Node:

    def __init__(self, component=None):
        self.component = component
        self.children = set({})
        self.parent = None
        if component is None:
            self.name = "GOD"
        else:
            self.name = component.get_name()
    #
    # def set_parent(self, parent):
    #     if self.parent is None:
    #         self.parent = parent
    #     else:
    #         print("DTOIASJDFLKAJDSGOIAWJGOIEWJGWOIJWOEj HIER MUSS WAS PASSIEREN!")

    def add_child(self, node):
        self.children.add(node)

    def as_dict(self):
        return {
            "name": self.name,
            "children": self._child_dict()
        }

    def _child_dict(self):
        result = []
        for child in self.children:
            result.append(child.as_dict())
        return result

    def find(self, component):
        for child in self.children:
            if child.component is component:
                return child
            else:
                return child.find(component)

    def get_root(self):
        if self.parent is None:
            return self
        else:
            return self.parent.get_root()