#  Copyright (c) 2023. Stefan Eiermann
#  Licenced under AGPL see /LICENSE

import plotly.express as px
from cmptree.utils.circuit.circuit import Circuit


class TreeMap:
    @classmethod
    def get_tree(cls, mainpart, *args):
        name_list = []
        parent_list = []
        res = mainpart.filtered_tree(*args, use_global=True)

        def resolve(data):
            for item in data.get("children", []):
                name_list.append(item.get("name"))
                parent_list.append(data.get("name"))
                resolve(item)

        if type(res) is list:
            res = {"name": "root", "children": res}
        resolve(res)

        return name_list, parent_list

    def show_tree_to_end(self, *args, **kwargs):
        name_list, parent_list = self.get_tree(*args, **kwargs)
        fig = px.treemap(names=name_list, parents=parent_list, maxdepth=-1)
        fig.update_traces(root_color="lightgrey")
        fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
        fig.show()
