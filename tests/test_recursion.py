import pytest
from basecomponents import Component, DimensionComponent, ThermalComponent, ElectricComponent, ElectricSignal
from collections import namedtuple
import numpy as np
from pytest_unordered import unordered


@pytest.fixture()
def tree():
    world = Component(name="world")
    ThermalComponent(world)
    DimensionComponent(world)

    akw = Component(name="akw")
    DimensionComponent(akw).set_parent(world)
    ThermalComponent(akw).set_parent(world)

    powerline = Component(name="powerline")
    ElectricComponent(powerline).set_parent(akw)

    streetlight = Component(name="streetlight")
    DimensionComponent(streetlight).set_parent(world)
    ElectricComponent(streetlight).set_parent(powerline)

    home = Component(name="home")
    DimensionComponent(home).set_parent(world)
    ElectricComponent(home).set_parent(powerline)
    ThermalComponent(home).set_parent(world)

    table = Component(name="table")
    DimensionComponent(table).set_parent(home)

    lamp = Component(name="lamp")
    DimensionComponent(lamp).set_parent(home)
    ElectricComponent(lamp).set_parent(home)

    Treedata = namedtuple("Tree", ("world", "home", "akw", "powerline", "table", "streetlight", "lamp"))

    return Treedata(world,home,akw,powerline,table, streetlight, lamp)

def test_fixture(tree):

    #assert tree.world.children_components["dimension"] == set({table})
    #assert table.parent_components["dimension"] == tree.home
    pass





def test_set_parent():
    world = Component(name="world")
    DimensionComponent(world)
    home = Component(name="home")
    DimensionComponent(home).set_parent(world)
    table = Component(name="table")
    DimensionComponent(table).set_parent(home)

    assert world.children_components["dimension"]["generic"] == set({home})
    assert home.children_components["dimension"]["generic"] == set({table})
    assert table.parent_components["dimension"]["generic"] == home
    assert home.parent_components["dimension"]["generic"] == world

    chair = Component(name="chair")
    DimensionComponent(chair).set_parent(home)

    assert world.children_components["dimension"]["generic"] == set({home})
    assert home.children_components["dimension"]["generic"] == set({table, chair})
    assert table.parent_components["dimension"]["generic"] == home
    assert home.parent_components["dimension"]["generic"] == world

    ThermalComponent(world)
    ThermalComponent(home).set_parent(world)

    assert world.children_components["dimension"]["generic"] == set({home})
    assert world.children_components["thermal"]["generic"] == set({home})
    assert home.children_components["dimension"]["generic"] == set({table, chair})
    assert table.parent_components["dimension"]["generic"] == home
    assert home.parent_components["dimension"]["generic"] == world
    assert home.parent_components["thermal"]["generic"] == world

def test_build_tree_simple_filter(tree):
    res = tree.world.filterd_tree("dimension")

    assert res.as_dict() == {
        "name": "world",
        "children": unordered([
            {
                "name": "home",
                "children": unordered([{
                    "name": "table",
                    "children": []
                },{
                    "name": "lamp",
                    "children": []
                }])
            },
            {
                "name": "streetlight",
                "children": []
            },
            {
                "name": "akw",
                "children": []
            }
        ])
    }

def test_build_tree_electric_filter(tree):
    res = tree.akw.filterd_tree("electric")
    assert res.as_dict() == {
        "name": "akw",
        "children": unordered([
            {
                "name": "powerline",
                "children": unordered([
                    {
                        "name": "streetlight",
                        "children": []
                    },
                    {
                        "name": "home",
                        "children": [{
                            "name": "lamp",
                            "children": []
                        }]
                    },
                ])
            }
        ])
    }


def test_build_tree_electric_filter(tree):
    res = tree.akw.filterd_tree("electric", ElectricSignal.POWER_LVL_5)
    assert res.as_dict() == {
        "name": "akw",
        "children": []
    }

def test_set_parent_for_electric_signals():
    akw = Component(name="akw")
    ElectricComponent(akw)

    powerline = Component(name="powerline")
    ElectricComponent(powerline).set_parent(akw, ElectricSignal.POWER_IN)

    streetlight = Component(name="streetlight")
    ElectricComponent(streetlight).set_parent(powerline)

    assert powerline.children_components["electric"]["generic"] == set({streetlight})

    res = akw.filterd_tree("electric", ElectricSignal.POWER_IN)

    assert res.as_dict() == {
        "name": "akw",
        "children": [{"name":"powerline", "children": []}]
    }