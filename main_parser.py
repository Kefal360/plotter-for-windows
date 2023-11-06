
import sys
import os

from expr_parser import Parser
expression = input("Input math expression: ")

parser = Parser(expression)

print("Variables in your expression: " + ", ".join(parser.variables_names))

variables = {}

for key in parser.variables_names:
    variables[key] = float(input(f"Input '{key}' variable value: "))

res = parser.evaluate(variables)

print(f"Evaluation result is: {res}")
