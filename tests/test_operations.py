from pyterator import iterate
from pyterator.operations import OPS


def test_contains():
    container = [1, 2, 3]
    fn = OPS["in"]
    assert fn(1, container) == True


def test_getitem():
    container = [97, 98, 99]
    fn = OPS["[]"]
    assert fn(container, 0) == 97

# We will just test using map


def test_map_contains():
    assert iterate([1, 99, 96, 97]).map("in", [1, 2, 3]).to_list() \
        == [True, False, False, False]


def test_map_getitem():
    assert iterate([("apple", "orange", "car"), ("fan", "mirror", "clock"), ("fridge", "chair", "jug")]).map("[]", 2).to_list() \
        == ["car", "clock", "jug"]
