import components as cmp
import plotly.express as px
from basecomponents import ElectricSignal as ES


def get_tree_to_end(maincomponent, *args):
    name_list = []
    parent_list = []

    res = maincomponent.filtered_tree(*args, use_global=True)

    def resolve(data):
        for item in data.get("children",[]):
            name_list.append(item.get("name"))
            parent_list.append(data.get("name"))
            resolve(item)


    if type(res) is list:
        res = {
            "name": "root",
            "children": res
        }

    resolve(res)

    return name_list, parent_list


def show_tree_to_end(*args, **kwargs):
    name_list, parent_list = get_tree_to_end(*args, **kwargs)

    fig = px.treemap(
        names=name_list,
        parents=parent_list,
        maxdepth=-1
    )
    fig.update_traces(root_color="lightgrey")
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    fig.show()


def wrapper(*args):
    name_list = []
    parent_list = []

    def get_all_trees(world, *args):
        x = world.get_all_children()
        pass

    get_all_trees(*args)
    return name_list, parent_list