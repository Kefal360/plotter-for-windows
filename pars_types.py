from collections.abc import Callable
from enum import Enum, auto

import numpy as np

ValueType = int | float | np.ndarray

FunctionType = Callable[[ValueType], ValueType]

OperatorType = Callable[[ValueType, ValueType], ValueType]


class Token(Enum):
    Variable = auto()
    Number = auto()
    Function = auto()
    Operator = auto()
    LBrace = auto()
    RBrace = auto()
    Space = auto()


TokenType = tuple[str | float, Token]
