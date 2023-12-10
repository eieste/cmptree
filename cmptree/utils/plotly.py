#  Copyright (c) 2023. Stefan Eiermann
#  Licenced under AGPL see /LICENSE

import plotly.express as px
from utils.circuit.circuit import Circuit


def get_tree_to_end(maincomponent, *args):
    name_list = []
    parent_list = []
    res = maincomponent.filtered_tree(*args, use_global=True)

    def resolve(data):
        for item in data.get("children", []):
            name_list.append(item.get("name"))
            parent_list.append(data.get("name"))
            resolve(item)

    if type(res) is list:
        res = {"name": "root", "children": res}
    resolve(res)

    return name_list, parent_list


def show_tree_to_end(*args, **kwargs):
    name_list, parent_list = get_tree_to_end(*args, **kwargs)

    fig = px.treemap(names=name_list, parents=parent_list, maxdepth=-1)
    fig.update_traces(root_color="lightgrey")
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    fig.show()


def get_circuits():

    for cmp in cmp.Component.all_components:
        # check if ci

        for signal_name, item_list in cmp.child_parts.get("electric", {}).items():

            for circuit in Circuit.all_circuits:
                for member in circuit.members:

                    if cmp.is_connected(member, "electric", signal_name):
                        circuit = Circuit.search(cmp)

        if not circuit:
            pass
