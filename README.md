# Pyterator

Write fluent functional programming idioms in Python.

- Chain operations like `map`, `reduce`, `filter_map`
- Lazy evaluation

Readable transformation functions, as opposed to Lisp-ish prefix notation-esque map filter functions.

---

## Contents

- [Installation](#installation)
- [Quick start](#quick-start)
- [How it works](#how-it-works)
- [Motivation](#motivation)
- [Design](#design)
- [How is it different?](#how-it-works)
- [Who is this for (and not for)?](#anyone)
- [Design](#design)
- [Examples](#examples)

## Installation

```bash
pip install git+https://github.com/remykarem/pyterator.git#egg=pyterator
```

## Quick start

```python
>>> from pyterate import iterate
```

```python
>>> text = ["hello", "world"]
>>> iterate(text).map(str.upper).to_list()
['HELLO', 'WORLD']
```

Chain operations

```python
>>> text = ["hello", "my", "love"]
>>> (
...     iterate(text)
...     .filterfalse(lambda x: x in ["a", "my"])
...     .map(str.upper)
...     .map(lambda x: x+"!")
...     .to_list()
... )
['HELLO!', 'LOVE!']
```

## Motivation

Using `map`, `reduce` in Python forces you to write in prefix notation-esque which makes it hard to read.

For a transformation pipeline:

```python
[1, 2, 3, 4] -> [2, 3, 4, 5] -> [3, 5] -> 15
```

Python:

```python
reduce(lambda x,y: x * y,
    filter(lambda x: x % 2,
        map(lambda x: x+1, [1, 2, 3, 4])), 1)
```

which looks similar to Clojure (or Lisp-like)

```clojure
(reduce *
    (filter even?
        (map (fn [x] (+ 1 x)) '(1 2 3 4))))
```

and Haskell

```haskell
foldl (*) 1 
    (filter odd 
        (map (\x -> x+1) [1, 2, 3, 4]))
```

which are languages where prefix notation is their natural syntax.

List comprehensions, while idiomatic and commonplace among  developers, can be hard to read at times.

## Design

This design is largely influenced by modern languages that implement functional programming idioms like Rust, Kotlin, Scala and JavaScript. The Apache Spark framework, which is written in Scala, largely exposes functional programming idioms in the Python APIs.

We want the subject of the chain of transformations to be the data itself, then call the operations in succession:

```python
(
    [1,2,3,4]
    .map(...)
    .filter(...)
    .reduce(...)
)
```

and

```python
(
    iter([1,2,3,4])
    .map(...)
    .filter(...)
    .reduce(...)
)
```

Since Python's iterator does not have methods `map`, `reduce`, we implemented our own `iterate`, which is similar to Python's builtin `iter`, so that client code can easily switch it out.

```python
(
    iterate([1,2,3,4])
    .map(...)
    .filter(...)
    .reduce(...)
)
```

iterator,

It is also a builder function, which returns a `_Pyterator` instance that implements `__next__`.

## How it works

Lazy. Reduce operations and to_list() operations will 'materialise' your transformations.

## Examples

### Example 1: Square

```txt
[1, 2, 3, 4] -> [1, 4, 9, 16]
```

```python
>>> from pyterator import iterate
>>> nums = [1, 2, 3, 4]
```

Pyterator

```python
>>> iterate(nums).map(lambda x: x**2).to_list()
```

List comprehension

```python
>>> [x**2 for x in nums]
```

Map reduce

```python
>>> list(map(lambda x: x**2, iter(nums)))
```

### Example 2: Filter

Pyterator

```python
>>> iterate(nums).filter(lambda x: x > 3).to_list()
```

List comprehension

```python
>>> [x for x in nums if x > 3]
```

### Flat map

```python
[
"peter piper",
"picked a peck",     ->
"of pickled pepper",
]
```

List comprehension

```python
>>> [word for text in texts for word in text.split()]
```

Pyterator

```python
>>> iterate(texts).flat_map(str.split).to_list()
```

### Multiple transformations

```python
>>> from pyterator import iterate
>>> stopwords = {"of", "a"}
>>> texts = [
    "peter piper Picked a peck  ",
    "of Pickled pePper",
    "\na peck of pickled pepper peter piper picked",
]
```

List comprehension

```python
>>> words = [
        word for text in texts
        for word in text.lower().strip().split()
        if word not in stopwords]
>>> set(words)
{'peck', 'pepper', 'peter', 'picked', 'pickled', 'piper'}
```

Pyterator

```python
>>> (
...     iterate(texts)
...     .map(str.strip)
...     .map(str.lower)
...     .flat_map(str.split)
...     .filter(lambda word: word not in stopwords)
...     .to_set()
... )
{'peck', 'pepper', 'peter', 'picked', 'pickled', 'piper'}
```

## Inspired by

https://doc.rust-lang.org/std/iter/trait.Iterator.html

## Gotchas

These gotchas pertain to mutability of the collections

## What this is not for

Vectorised operations - use NumPy or other equivalent

## API

common

- `map`
- `enumerate`
- `filter`
- `for_each`
- `filterfalse`
- `filter_map`
- `starmap`
- `starfilter`
- `star_map_filter`

order

- `reverse`

dimension change

- `partition`
- `flat_map`
- `star_flat_map`
- `chunked`
- `flatten`
- `zip`
- `chain`

positional

- `skip`
- `first`
- `nth`
- `take`

collect

- `to_list`
- `to_set`
- `to_dict`
- `groupby`

reduce

- `reduce`
- `all`
- `any`
- `min`
- `max`
- `sum`
- `prod`
- `join`
- `sample`

## Similar libraries

Note that these libraries focus on fluent method chaining.

- [PyFunctional](https://github.com/EntilZha/PyFunctional)
- [fluent](https://github.com/dwt/fluent)
