from dataclasses import dataclass

import numpy as np

from pars_types import FunctionType, OperatorType, ValueType


# Additional functions that are not defined in numpy


def acot(x: ValueType):
    return np.arctan(1 / x)


def cot(x: ValueType):
    return 1 / np.tan(x)


# Function and operation names to evaluators mapping


functions: dict[str, FunctionType] = {
    "abs": np.abs,
    "acos": np.arccos,
    "acosh": np.arccosh,
    "acot": acot,
    "asin": np.arcsin,
    "asinh": np.arcsinh,
    "atan": np.arctan,
    "avg": np.average,
    "cos": np.cos,
    "cosh": np.cosh,
    "cot": cot,
    "exp": np.exp,
    "inf": np.inf,
    "lg": np.log10,
    "ln": np.log,
    "log10": np.log10,
    "log2": np.log2,
    "max": np.max,
    "min": np.min,
    "prod": np.prod,
    "sgn": np.sign,
    "sign": np.sign,
    "sin": np.sin,
    "sinh": np.sinh,
    "sqrt": np.sqrt,
    "sum": np.sum,
    "sup": np.max,
    "tanh": np.tanh,
    "tan": np.tan,
}

operators: dict[str, OperatorType] = {
    "+": np.add,
    "-": np.subtract,
    "*": np.multiply,
    "/": np.divide,
    "%": np.mod,
    "^": np.float_power,
}

priorities: dict[str, int] = {
    "(": 0,
    "+": 1,
    "-": 1,
    "*": 2,
    "/": 2,
    "%": 2,
    "^": 3,
    "f": 4,  # function
    ")": 5,
}


@dataclass
class Operation:
    """
    Base class for math operation token (function, brace, operator).
    It stores the way it is evaluated, evaluation priority and number
    of arguments it supports.
    """

    evaluator: (FunctionType | OperatorType | str)
    priority: int
    size: int


class FunctionOperation(Operation):
    """
    `Operator` class factory that represents function
    """

    def __init__(self, name: str):
        super().__init__(functions[name], priorities["f"], 1)


class BraceOperation(Operation):
    """
    `Operator` class factory that represents brace
    """

    def __init__(self, name: str):
        super().__init__(name, priorities[name], 0)


class OperatorOperation(Operation):
    """
    `Operator` class factory that represents binary operator
    """

    def __init__(self, name: str):
        super().__init__(operators[name], priorities[name], 2)
