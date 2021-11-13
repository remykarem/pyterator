from pyterator import iterate

nums = [1, 2, 3, 4, 5]


def test_iterate():
    assert iterate(nums).to_list() == list(iter(nums))