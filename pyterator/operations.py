import math
import operator

# The context element should always be on LHS
OPS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "÷": operator.truediv,
    "%": operator.mod,
    "^": operator.xor,
    "==": operator.eq,
    "!=": operator.ne,
    ">": operator.gt,
    "<": operator.lt,
    "≥": operator.ge,
    ">=": operator.ge,
    "≤": operator.le,
    "<=": operator.le,
    "in": lambda el, container: operator.contains(container, el),
    "**": operator.pow,
    "√": math.sqrt,
    "[]": operator.getitem,
}