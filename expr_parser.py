from expression import BinaryExpression, Expression, UnaryExpression, ValueExpression
from operation import (
    BraceOperation,
    FunctionOperation,
    Operation,
    OperatorOperation,
    priorities,
)
from tokenizer import Token, Tokenizer
from pars_types import ValueType
from constants_parser import CONSTANTS


class Parser:
    """
    Class that accepts math expression in its constructor,
    parses it and provides `evaluate` method to substitue
    variables values to it
    """

    def __init__(self, input_expr: str):
        self.input_expr = input_expr
        self.variables_names: set[str] = set()

        self._tokenize()
        self._parse()

    def _tokenize(self):
        """
        Uses `Tokenizer` class for math expression splitting
        """
        self.tokens = Tokenizer(self.input_expr)

    def _parse(self):
        """
        Generates an evaluation tree from tokens by utilizing two
        stacks - one for values and one for operations. Values and
        operations are placed into corresponding stacks, and when
        possible, assempled into tree node.
        """
        self.val_stack: list[Expression] = []
        self.op_stack: list[Operation] = []

        for t_val, t_type in self.tokens:
            if t_type in (Token.Number, Token.Variable):
                self.val_stack.append(ValueExpression(t_val))

                if t_type == Token.Variable:
                    self.variables_names.add(t_val)

            elif t_type == Token.Function:
                self.op_stack.append(FunctionOperation(t_val))

            elif t_type == Token.LBrace:
                self.op_stack.append(BraceOperation("("))

            elif t_type == Token.RBrace:
                while len(self.op_stack) > 0 and not (
                    self.op_stack[-1].size == 0 and self.op_stack[-1].priority == 0
                ):  # until next in stack is lbrace
                    self._do_one()
                self.op_stack.pop()  # pop lbrace

            elif t_type == Token.Operator:
                t_priority = priorities[t_val]

                while (
                    len(self.op_stack) > 0 and self.op_stack[-1].priority > t_priority
                ):
                    self._do_one()

                self.op_stack.append(OperatorOperation(t_val))

        while len(self.op_stack) > 0:
            self._do_one()

        self._evaluator = self.val_stack[0].evaluate

        self.__debug_expr = repr(self.val_stack)

    def _do_one(self):
        """
        Assembles one operation into `Expression` tree node that is stored
        on value stack.
        """
        op = self.op_stack.pop()

        if op.size == 1:
            a = self.val_stack.pop()
            self.val_stack.append(UnaryExpression(op.evaluator, a))
        elif op.size == 2:
            b, a = self.val_stack.pop(), self.val_stack.pop()  # inversed pop order
            self.val_stack.append(BinaryExpression(op.evaluator, a, b))

    def evaluate(self, variables: dict[str, ValueType]):
        """
        Evaluates supplied to constructor expression with provided 
        variables values
        """
        variables |= CONSTANTS
        return self._evaluator(variables)

    def __repr__(self):
        return self.__debug_expr
