"""
Contains classes for expression tree representation and evaluation
"""

import abc
from collections.abc import Callable, Mapping

from pars_types import FunctionType, OperatorType, ValueType


class Expression(abc.ABC):
    """
    Abstract base class for a single parsed expression as a tree data
    structure. It also defines its public function for triggering
    evaluation. Each child class sets `_evaluator` property to a
    function that accepts variables values and produces numpy array.
    """

    _evaluator: Callable[[Mapping[str, ValueType]], ValueType]

    def evaluate(self, variables: Mapping[str, ValueType]):
        return self._evaluator(variables)


class ValueExpression(Expression):
    """
    This expression accepts variable name, numpy array or scalar number
    and evaluates to either constant or variable value, corresponding
    to its name.
    """

    def __init__(self, a: str | ValueType):
        self.__debug_a = a

        if isinstance(a, str):
            self._evaluator = lambda vars: vars[a]
        else:
            self._evaluator = lambda _: a

    def __repr__(self):
        return f"<{self.__debug_a}>"


class UnaryExpression(Expression):
    """
    This expression accepts function with one argument and `Expression`
    (value, unary or binary) and that function on expression, passed into it.
    It is applied for named functions like `exp(a)`
    """

    def __init__(self, function: FunctionType, a: Expression):
        self.__debug_f = function.__name__
        self.__debug_a = repr(a)

        self._evaluator = lambda vars: function(a.evaluate(vars))

    def __repr__(self):
        return f"<{self.__debug_f}({self.__debug_a})>"


class BinaryExpression(Expression):
    """
    This expression is similar to `UnaryExpression`, but accepts function
    with two arguments and two expressions.
    It is applied for math operators like `a - b`
    """

    def __init__(
        self,
        function: OperatorType,
        a: Expression,
        b: Expression,
    ):
        self.__debug_f = function.__name__
        self.__debug_a = repr(a)
        self.__debug_b = repr(b)

        self._evaluator = lambda vars: function(a.evaluate(vars), b.evaluate(vars))

    def __repr__(self):
        return f"<{self.__debug_a} {self.__debug_f} {self.__debug_b}>"
