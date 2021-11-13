from pyterator import iterate

nums = [1, 2, 3, 4, 5]


def test_map():
    assert iterate(nums).map(lambda x: x+1).to_list() \
        == list(map(lambda x: x+1, nums))


def test_map_shorthand_ops():
    assert iterate(nums).map("+", 2).to_list() \
        == list(map(lambda x: x+2, nums))


def test_map_custom_function():
    def add(x, y):
        return x + 8*y

    assert iterate(nums).map(add, 5).to_list() \
        == list(map(lambda x: add(x, 5), nums))
