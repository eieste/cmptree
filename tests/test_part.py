#  Copyright (c) 2023. Stefan Eiermann
#  Licenced under AGPL see /LICENSE

from cmptree.part import Part


class TestCharacteristics:
    def __init__(self, part):
        self.part = part

    def get_name(self):
        return "test-characteristic"


def test_part():
    newpart = Part(name="test")
    assert newpart in Part.all_parts


def test___str__():
    newpart = Part(name="test")
    assert str(newpart) == '<Part name="test">'


def test_get_name():
    newpart = Part(name="test")
    assert newpart.get_name() == "test"


def test_has():
    newpart = Part(name="test")
    assert newpart.has("test") == False
    newpart.characteristics["test"] = "test"
    assert newpart.has("test") == True


def test_get():
    newpart = Part(name="test")
    assert newpart.get("test") == None
    newpart.characteristics["test"] = "test"
    assert newpart.get("test") == "test"


def test_attach_characteristics():

    characteristic = TestCharacteristics(None)
    newpart = Part(name="test")
    newpart.attach_characteristic(characteristic)
    assert newpart.characteristics["test-characteristic"] == characteristic


def test_register_characteristic():

    newpart = Part(name="test")
    anotherpart = Part(name="test2")

    char = TestCharacteristics(anotherpart)
    newpart.register_characteristic(char)
    newpart.register_characteristic(char)
    newpart.register_characteristic(char)
    newpart.register_characteristic(char, "test")

    assert len(newpart.child_parts["test-characteristic"]["generic"]) == 1
    assert list(newpart.child_parts["test-characteristic"]["generic"])[0] == anotherpart
    assert list(newpart.child_parts["test-characteristic"]["test"])[0] == anotherpart


def test_goto_parent():
    newpart = Part(name="test")
    anotherpart = Part(name="test2")

    test_characteristic = TestCharacteristics(anotherpart)
    newpart.register_characteristic(test_characteristic)
    anotherpart.parent_parts["test-characteristic"] = {"generic": newpart}

    assert anotherpart.goto_parent("test-characteristic", "generic") == newpart
