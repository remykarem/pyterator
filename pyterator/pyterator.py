from __future__ import annotations

from functools import reduce
from collections import Counter
from collections.abc import Iterable
from typing import Any, Callable, Generator, Iterator, List, Tuple, Optional
from itertools import chain, filterfalse, islice, product, starmap
from itertools import tee as _tee

from more_itertools import (
    chunked, map_reduce, sample, partition, islice_extended,
    split_at, windowed
)


def iterate(iterable: Iterable[Any]) -> _Pyterator:
    """Similar to the builtin `iter` object"""
    return _Pyterator(iterable)


def tee(iterable: Iterable[Any], n: int = 2) -> List[_Pyterator]:
    """Similar to `itertools.tee`"""
    iters = _tee(iterable, n)
    return [_Pyterator(it) for it in iters]


class _Pyterator:

    def __init__(self, iterable: Iterable):
        self.__iterator = iter(iterable)

    def __repr__(self) -> str:
        return f"<pyterator at {hex(id(self))}>"

    def __iter__(self) -> Iterator:
        return self.__iterator

    def __next__(self) -> Any:
        return next(self.__iterator)

    def reverse(self) -> _Pyterator:
        """Reverses the order of the elements in the underlying iterator

        Returns:
            _Pyterator: _Pyterator object
        """
        self.__iterator = islice_extended(self.__iterator, -1, None, -1)
        return self

    def map(self, fn: Callable) -> _Pyterator:
        """Similar to the builtin `map` object. Returns an iterator
        yielding the results of applying the function to the items of
        iterable.

        Args:
            fn (Callable): Function to apply to each item

        Returns:
            _Pyterator: _Pyterator object
        """
        self.__iterator = map(fn, self.__iterator)
        return self

    def starmap(self, fn: Callable) -> _Pyterator:
        """Similar to the `itertools.starmap` object. Applies function to
        arguments obtained from every item in the underlying iterator.

        Args:
            fn (Callable): Function to apply to each item

        Returns:
            _Pyterator: _Pyterator object
        """
        self.__iterator = starmap(fn, self.__iterator)
        return self

    def filter(self, predicate_fn: Callable) -> _Pyterator:
        """Similar to the builtin `filter`. Yields items of iterable for which
        function(item) is true. If function is None, return items that are true.

        Args:
            predicate_fn (Callable): Predicate

        Returns:
            _Pyterator: Pyterator object
        """
        self.__iterator = filter(predicate_fn, self.__iterator)
        return self
    
    def starfilter(self, fn: Callable) -> _Pyterator:
        """Similar to the builtin `filter`. Yields items of iterable for which
        function(*item) is true. If function is None, return items that are true.

        Args:
            fn (Callable): Predicate

        Returns:
            _Pyterator: _Pyterator object
        """
        self.__iterator = filter(lambda args: fn(*args), self.__iterator)
        return self

    def filterfalse(self, fn: Callable) -> _Pyterator:
        self.__iterator = filterfalse(fn, self.__iterator)
        return self

    def filter_map(self, fn: Callable) -> _Pyterator:
        """
        Yields items of iterable for which fn(item) is truthy.

        Args:
            fn (Callable): Function to apply to each item
        
        Returns:
            _Pyterator: _Pyterator object
        """
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

    def enumerate(self, start: int = 0) -> _Pyterator:
        """Similar to the builtin `enumerate` object. Yields a tuple containing
        an index and a value from the iterable.

        Args:
            start (int, optional): Start index. Defaults to 0.

        Returns:
            _Pyterator: Pyterator object
        """
        self.__iterator = enumerate(self.__iterator, start)
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
    
    def split_at(self, predicate_fn: Callable) -> Generator[_Pyterator]:
        for it in split_at(self.__iterator, predicate_fn):
            yield _Pyterator(it)
    
    def product(self, *iterables: Iterable) -> _Pyterator:
        """Cartesian product"""
        self.__iterator = product(self.__iterator, *iterables)
        return self
    
    def windowed(self, window_size: int, step: int, fillvalue: Optional[Any] = None):
        self.__iterator = windowed(self.__iterator, window_size, step=step, fillvalue=fillvalue)
        return self

    def unique_everseen(self, key=None) -> _Pyterator:
        """
        Yield unique elements, preserving order. Remember all elements ever seen.
        """
        return _Pyterator(_unique_everseen(self.__iterator, key))

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

    def first(self, default: Optional[Any] = None) -> Any:
        """Returns the first element of the iterator.

        Args:
            default (Any, optional): Value to return if there is no element
                in the iterator. Defaults to None.

        Returns:
            Any: First element of the iterator
        """
        return next(self.__iterator, default)

    def nth(self, n: int, default: Optional[Any] = None) -> Any:
        """Returns the nth element of the iterator.
        If n is larger than the length of the iterator, return default.
        The underlying iterator is advanced by n elements.

        Args:
            n (int): Index of element to return
            default (Any, optional): Value to return is n is larger
                than the length of iterator. Defaults to None.

        Returns:
            Any: nth element of the iterator
        """
        return next(islice(self.__iterator, n, None), default)

    def islice(self, *args: int) -> Iterator[Any]:
        """Returns the next n elements. Similar to itertools.islice.
        The underlying iterator will be advanced by n elements. 

            >>> iterate([9, 8, 7]).islice(2)
            [9, 8]
            >>> iterate([9, 8, 7]).islice(2, 3)
            [7]
            >>> iterate([9, 8, 6, 5, 7, 4]).islice(1, 6, 2)
            [8, 5, 4]

        Args:
            n (int): No. of elements to return

        Returns:
            Iterator: Iterator object
        """
        return islice(self.__iterator, *args)

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
        """
        Returns a list from the iterable's elements.

        Returns:
            list: List of elements
        """
        return list(self.__iterator)
    
    def to_tuple(self) -> tuple:
        """
        Returns a tuple from the iterable's elements.

        Returns:
            tuple: Tuple of elements
        """
        return tuple(self.__iterator)

    def to_set(self) -> set:
        """
        Returns a set from the iterable's elements.

        Returns:
            set: Set of elements
        """
        return set(self.__iterator)

    def to_dict(self) -> dict:
        """
        Returns a dictionary from the iterable's elements. The keys are the elements.
        """
        return dict(self.__iterator)

    def to_counter(self) -> dict:
        """
        Returns a count from the iterable's elements. The keys are the elements.
        """
        return Counter(self.__iterator)

    def groupby(self, *args) -> dict:
        return map_reduce(self.__iterator, *args)

    ### Reduce functions ###

    def sample(self, k: int = 1) -> Any:
        """Return a *k*-length list of elements chosen (without replacement)
        from the *iterable*. Like :func:`random.sample`, but works on iterables
        of unknown length."""
        return sample(self.__iterator, k)

    def reduce(self, fn: Callable, initial: Optional[Any] = None) -> Any:
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

    def max(self) -> Any:
        """Gets the max of all elements in the iterable.

        Returns:
            Any: Max of all elements in the iterable.
        """
        return max(self.__iterator)

    def min(self) -> Any:
        """Gets the min of all elements in the iterable.

        Returns:
            Any: Min of all elements in the iterable.
        """
        return min(self.__iterator)

    def sum(self) -> Any:
        """Gets the sum of all elements in the iterable.

        Returns:
            Any: Sum of all elements in the iterable.
        """
        return sum(self.__iterator)

    def prod(self) -> Any:
        """Gets the product of all elements in the iterable.

        Returns:
            Any: Product of all elements in the iterable.
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
    
    ### Debug ###

    def debug(self) -> None:
        """
        Creates a REPL-like interface for debugging. Best used in an IPython-like environment.
        Not for use in production.

        Current iterator will not be consumed because an independent iterator is returned.
        """
        # Create an independent iterator for debugging
        self.__iterator, iterator = _tee(self.__iterator)

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

def _unique_everseen(iterable, key=None):
    """From https://docs.python.org/3/library/itertools.html
    List unique elements, preserving order. Remember all elements ever seen.

    >>> _unique_everseen('AAAABBBCCDAABBB') --> A B C D
    >>> _unique_everseen('ABBCcAD', str.lower) --> A B C D
    """
    seen = set()
    seen_add = seen.add
    if key is None:
        for element in filterfalse(seen.__contains__, iterable):
            seen_add(element)
            yield element
    else:
        for element in iterable:
            k = key(element)
            if k not in seen:
                seen_add(k)
                yield element
