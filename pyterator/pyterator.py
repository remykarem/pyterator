from typing import Any, Callable, Generator, Union
from itertools import chain, islice
from itertools import starmap as _starmap
from pyterator.operations import OPS
from functools import reduce as _reduce
from more_itertools import chunked as _chunked
from more_itertools import map_reduce as _map_reduce
from more_itertools import sample as _sample
from more_itertools import partition as _partition
from more_itertools import islice_extended

_map = map
_filter = filter
_sum = sum
_max = max
_min = min
_zip = zip


def iterate(iterable, deepcopy=False):
    """Similar to the builtin `iter` object"""
    return _Pyterator(iterable)


def rev_iterate(iterable):
    return _Pyterator(_reverse(iterable))


def _reverse(iterable):
    """https://stackoverflow.com/questions/529424/traverse-a-list-in-reverse-order-in-python

    Args:
        iterable ([type]): [description]

    Yields:
        [type]: [description]
    """
    for i in range(len(iterable)-1, -1, -1):
        yield iterable[i]


class _Pyterator:

    def __init__(self, iterable):
        self.__iterator = iter(iterable)
        self.__push_front = None

    def __repr__(self):
        return f"<pyterator at {hex(id(self))}>"

    def __iter__(self):
        return self.__iterator

    def __next__(self):
        print("next")
        if self.__push_front:
            print(self.__push_front)
            val = self.__push_front
            self.__push_front = None
            return next(self.__iterator, val)
        else:
            return next(self.__iterator)

    def reverse(self):
        self.__iterator = islice_extended(self.__iterator, -1, None, -1)
        return self

    def map(self, fn: Callable, *rhs):
        if isinstance(fn, str):
            fn = OPS[fn]
        if rhs:
            self.__iterator = _map(lambda lhs: fn(lhs, *rhs), self.__iterator)
        else:
            self.__iterator = _map(lambda lhs: fn(lhs), self.__iterator)
        return self

    def starmap(self, fn):
        if isinstance(fn, str):
            fn = OPS[fn]
        self.__iterator = _starmap(fn, self.__iterator)
        return self

    def filter(self, predicate_fn: Callable, *rhs):
        if isinstance(predicate_fn, str):
            predicate_fn = OPS[predicate_fn]
        if rhs:
            self.__iterator = _filter(
                lambda lhs: predicate_fn(lhs, *rhs), self.__iterator)
        else:
            self.__iterator = _filter(predicate_fn, self.__iterator)
        return self

    def filter_not(self, fn: Callable, *rhs):
        if isinstance(fn, str):
            fn = OPS[fn]
        if rhs:
            self.__iterator = _filter(
                lambda lhs: not fn(lhs, *rhs), self.__iterator)
        else:
            self.__iterator = _filter(lambda: not fn(), self.__iterator)
        return self

    def filter_map(self, fn: Callable, *rhs):
        self.map(fn, *rhs)
        self.__iterator = _filter(lambda x: x, self.__iterator)
        return self

    def for_each(self, fn: Callable, *rhs):
        if rhs:
            fn(*rhs)
        else:
            fn()

    def enumerate(self):
        self.__iterator = enumerate(self.__iterator)
        return self

    ### Advanced Operations ###

    def flat_map(self, fn: Callable, *rhs):
        return self.map(fn, *rhs).flatten()

    def flatten(self):
        "https://stackoverflow.com/questions/952914/how-to-make-a-flat-list-out-of-a-list-of-lists"
        self.__iterator = chain.from_iterable(self.__iterator)
        return self

    def partition(self, predicate_fn: Callable, *rhs):
        if isinstance(predicate_fn, str):
            predicate_fn = OPS[predicate_fn]
        if rhs:
            return _partition(lambda lhs: predicate_fn(lhs, *rhs), self.__iterator)
        else:
            return _partition(predicate_fn, self.__iterator)

    def chunked(self, n):
        self.__iterator = _chunked(self.__iterator, n)
        return self

    # Positional

    def skip(self, n: int):
        self.__iterator = islice(self.__iterator, n, None, 1)
        return self

    def first(self, default=None):
        return next(self.__iterator, default)

    def nth(self, n, default=None):
        return next(islice(self.__iterator, n, None), default)

    def take(self, n: int):
        self.__iterator = islice(self.__iterator, n)
        return self

    ### Collection methods ###

    def to_list(self) -> list:
        return list(self.__iterator)

    def to_gen(self) -> Generator:
        for x in self.__iterator:
            yield x

    def zip(self, iterable):
        self.__iterator = zip(self.__iterator, iterable)
        return self

    def to_set(self) -> set:
        """
        Return a set from the iterable's elements.

        Returns:
            set: 
        """
        return set(self.__iterator)

    def to_dict(self) -> dict:
        "Return a dictionary from the iterable's elements. The keys are the elements."
        return dict(self.__iterator)

    def groupby(self, *args):
        return _map_reduce(self.__iterator, *args)

    ### Reduce functions ###

    def sample(self, k: int = 1):
        return _sample(self.__iterator, k)

    def reduce(self, fn: Callable, *rhs):
        if isinstance(fn, str):
            fn = OPS[fn]
        if rhs:
            self.__iterator = _reduce(fn(self.__iterator, *rhs))
        else:
            self.__iterator = _reduce(fn(self.__iterator))
        return self

    def all(self) -> bool:
        """Return True if bool(x) is True for all values x in the iterable.

        If the iterable is empty, return True.

        Returns:
            bool: True if bool(x) is True for all values x in the iterable.
        """
        return all(self.__iterator)

    def any(self) -> bool:
        """Return True if bool(x) is True for any x in the iterable.

        If the iterable is empty, return False.

        Returns:
            bool: True if bool(x) is True for any x in the iterable.
        """
        return any(self.__iterator)

    def max(self) -> Union[int, float]:
        """Gets the max of all elements in the iterable.

        Returns:
            Union[int, float]: Max of all elements in the iterable.
        """
        return _max(self.__iterator)

    def min(self) -> Union[int, float]:
        """Gets the min of all elements in the iterable.

        Returns:
            Union[int, float]: Min of all elements in the iterable.
        """
        return _min(self.__iterator)

    def sum(self) -> Union[int, float]:
        """Gets the sum of all elements in the iterable.

        Returns:
            Union[int, float]: Sum of all elements in the iterable.
        """
        return _sum(self.__iterator)

    def prod(self) -> Union[int, float]:
        """Gets the product of all elements in the iterable.

        Returns:
            Union[int, float]: Product of all elements in the iterable.
        """
        return _reduce(lambda x, y: x * y, self.__iterator)

    def join(self, sep: str = "") -> str:
        """Concatenate any number of strings.

        Args:
            sep (str, optional): Separator. Defaults to "".

        Returns:
            str: Concatenated string
        """
        return sep.join(self.__iterator)

    ### Debug ###

    def debug(self):
        print("Hit ENTER for next value, q+ENTER to quit.")
        while True:
            v = input()
            if v.lower() == "q":
                break
            try:
                print(f"> {next(self)}", end=" ")
            except StopIteration:
                break
