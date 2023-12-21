import pytest
from cmptree.utils.plotly import TreeMap
from cmptree.part import Part
from cmptree.characteristic.base import BaseCharacteristic


@pytest.fixture
def robot(mocker):
    mocker.patch(
        "cmptree.characteristic.base.BaseCharacteristic.characteristic_name", "foo"
    )
    parts = {
        "world": Part(name="World"),
        "robot": Part(name="Robot"),
        "arm": Part(name="Arm"),
        "leg": Part(name="Leg"),
        "head": Part(name="Head"),
    }
    BaseCharacteristic(parts["robot"]).set_parent(parts["world"])
    BaseCharacteristic(parts["arm"]).set_parent(parts["robot"])
    BaseCharacteristic(parts["head"]).set_parent(parts["robot"])
    BaseCharacteristic(parts["leg"]).set_parent(parts["robot"])
    return parts


def test_get_tree(robot):
    name, parent = TreeMap.get_tree(robot["world"], "foo")
    assert sorted(["Arm", "Head", "Leg", "Robot", "World"]) == sorted(name)
    assert sorted(["Robot", "Robot", "Robot", "World", "root"]) == sorted(parent)
