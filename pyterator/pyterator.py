from __future__ import annotations

from functools import reduce
from collections.abc import Iterable
from typing import Any, Callable, Iterator, Tuple, Union
from itertools import chain, filterfalse, islice, tee, starmap

from more_itertools import (
    chunked, map_reduce, sample, partition, islice_extended,
    split_at
)


def iterate(iterable: Iterable[Any]) -> _Pyterator:
    """Similar to the builtin `iter` object"""
    return _Pyterator(iterable)


class _Pyterator:

    def __init__(self, iterable: Iterable):
        self.__iterator = iterable

    def __repr__(self) -> str:
        return f"<pyterator at {hex(id(self))}>"

    def __iter__(self) -> Iterator:
        return self.__iterator

    def __next__(self) -> Any:
        return next(self.__iterator)

    def reverse(self) -> _Pyterator:
        self.__iterator = islice_extended(self.__iterator, -1, None, -1)
        return self

    def map(self, fn: Callable) -> _Pyterator:
        self.__iterator = map(fn, self.__iterator)
        return self

    def starmap(self, fn: Callable) -> _Pyterator:
        self.__iterator = starmap(fn, self.__iterator)
        return self

    def filter(self, predicate_fn: Callable) -> _Pyterator:
        """Similar to the builtin filter. Returns an iterator yielding
        items of iterable for which function(item) is true. If function
        is None, return items that are true.

        Args:
            predicate_fn (Callable): Predicate

        Returns:
            _Pyterator: Pyterator object
        """
        self.__iterator = filter(predicate_fn, self.__iterator)
        return self
    
    def starfilter(self, fn: Callable) -> _Pyterator:
        self.__iterator = filter(lambda args: fn(*args), self.__iterator)
        return self

    def filterfalse(self, fn: Callable) -> _Pyterator:
        self.__iterator = filterfalse(fn, self.__iterator)
        return self

    def filter_map(self, fn: Callable) -> _Pyterator:
        self.map(fn)
        self.__iterator = filter(lambda x: x, self.__iterator)
        return self

    def star_filter_map(self, fn: Callable) -> _Pyterator:
        self.starmap(fn)
        self.__iterator = filter(lambda x: x, self.__iterator)
        return self

    def for_each(self, fn: Callable) -> None:
        for x in self.__iterator:
            fn(x)

    def enumerate(self) -> _Pyterator:
        self.__iterator = enumerate(self.__iterator)
        return self

    ### Dimensional ###

    def chain(self, *iterables: Iterable) -> _Pyterator:
        self.__iterator = chain(self.__iterator, *iterables)
        return self

    def zip(self, iterable: Iterable) -> _Pyterator:
        self.__iterator = zip(self.__iterator, iterable)
        return self

    def flat_map(self, fn: Callable) -> _Pyterator:
        return self.map(fn).flatten()

    def star_flat_map(self, fn: Callable) -> _Pyterator:
        return self.starmap(fn).flatten()

    def flatten(self):
        self.__iterator = chain.from_iterable(self.__iterator)
        return self

    def partition(self, predicate_fn: Callable) -> Tuple[_Pyterator, _Pyterator]:
        items_false, items_true = partition(predicate_fn, self.__iterator)
        return _Pyterator(items_true), _Pyterator(items_false)

    def chunked(self, n: int) -> _Pyterator:
        self.__iterator = chunked(self.__iterator, n)
        return self
    
    def split_at(self, predicate_fn: Callable) -> _Pyterator:
        self.__iterator = split_at(self.__iterator, predicate_fn)
        return self

    # Positional

    def skip(self, n: int) -> _Pyterator:
        """Creates an iterator that skips the first n elements.

        Args:
            n (int): No. of elements to skip

        Returns:
            _Pyterator: self
        """
        self.__iterator = islice(self.__iterator, n, None, 1)
        return self

    def first(self, default: Any = None) -> Any:
        """Returns the first element of the iterator.

        Args:
            default (Any, optional): Value to return if there is no element
                in the iterator. Defaults to None.

        Returns:
            Any: First element of the iterator
        """
        return next(self.__iterator, default)

    def nth(self, n: int, default: Any = None) -> Any:
        """Returns the nth element of the iterator.
        If n is larger than the length of the iterator, return default.

        Args:
            n (int): Index of element to return
            default (Any, optional): Value to return is n is larger
                than the length of iterator. Defaults to None.

        Returns:
            Any: nth element of the iterator
        """
        return next(islice(self.__iterator, n, None), default)

    def take(self, n: int) -> _Pyterator:
        """
        Yields the first n elements, or fewer if the underlying iterator
        ends sooner.

        Args:
            n (int): No. of elements to take

        Returns:
            _Pyterator: self
        """
        self.__iterator = islice(self.__iterator, n)
        return self

    ### Collection methods ###

    def to_list(self) -> list:
        return list(self.__iterator)

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

    def groupby(self, *args) -> dict:
        return map_reduce(self.__iterator, *args)

    ### Reduce functions ###

    def sample(self, k: int = 1) -> Any:
        """Return a *k*-length list of elements chosen (without replacement)
        from the *iterable*. Like :func:`random.sample`, but works on iterables
        of unknown length."""
        return sample(self.__iterator, k)

    def reduce(self, fn: Callable, initial: Any = None) -> Any:
        """
        Similar to `functools.reduce`. Apply a function of two arguments
        cumulatively to the items of a sequence from left to right.

        Args:
            fn (Callable): function to apply to every 2 items

        Returns:
            Any: result of the reduction
        """
        if initial:
            return reduce(fn, self.__iterator, initial)
        else:
            return reduce(fn, self.__iterator)

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
        return max(self.__iterator)

    def min(self) -> Union[int, float]:
        """Gets the min of all elements in the iterable.

        Returns:
            Union[int, float]: Min of all elements in the iterable.
        """
        return min(self.__iterator)

    def sum(self) -> Union[int, float]:
        """Gets the sum of all elements in the iterable.

        Returns:
            Union[int, float]: Sum of all elements in the iterable.
        """
        return sum(self.__iterator)

    def prod(self) -> Union[int, float]:
        """Gets the product of all elements in the iterable.

        Returns:
            Union[int, float]: Product of all elements in the iterable.
        """
        return reduce(lambda x, y: x * y, self.__iterator)

    def join(self, sep: str = "") -> str:
        """Concatenate any number of strings.

        Args:
            sep (str, optional): Separator. Defaults to "".

        Returns:
            str: Concatenated string
        """
        return sep.join(self.__iterator)
    
    def custom(self, fn: Callable, *args: Any, **kwargs: Any) -> _Pyterator:
        self.__iterator = fn(self.__iterator, *args, **kwargs)
        return self

    ### Debug ###

    def debug(self) -> None:
        """
        Creates a REPL-like interface for debugging. Best used in an IPython-like environment.
        Not for use in production.

        Current iterator will not be consumed because an independent iterator is returned.
        """
        # Create an independent iterator for debugging
        self.__iterator, iterator = tee(self.__iterator)

        print("Hit ENTER for next value, q+ENTER to quit.")
        while True:
            v = input()
            if v.lower() == "q":
                break
            try:
                print(f"> {next(iterator)}", end=" ")
            except StopIteration:
                print("End of iterator")
                break
