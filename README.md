# Math expression parser

Math expression evaluation library. It supports most of useful math operations and functions. Expressions can contain variables which can be substituted with `int`s, `float`s or `numpy.ndarray`s.

## Example usage

```python
from parser import Parser

parser = Parser("(-b + sqrt(b^2-4a c))/(2a)")

parser.variables_names # {'c', 'a', 'b'}

parser.evaluate({"a": 1, "b": -3, "c": 2}) # 1.0

parser.evaluate({"a": [1, 1, 1], "b": [-5, -6, -9], "c": [6, 9, 20]}) # [2. 3. 4.]
```
## Expression syntax

Expression can contain numbers or variable names with functions applied to them, separated with operators or united with braces. Numbers do not support `*`-less multiplication with spaces. Variables must be separated by space.

Here are examples with `_` as space

| Wrong | Right |
|--|--|
| `2_a` | `2a` or `2*a` |
| `a_2` | `a*2` |
| `a_2_a` | `a*2*a` |
| `2_cos(a)` | `2cos(a)` or `2*cos(a)` |
| `cos(a)_2` | `cos(a)*2` |
| `aa` | `a*a` or `a_a` |
| - | `cos(a)cos(a)` or `cos(a)_cos(a)` or `cos(a)*cos(a)` |


Theese are supported:

Functions: 

| name | math |
|--|--|
| `abs` | $\|x\|$ |
| `acos` | $\cos^{-1}(x)$ |
| `acosh` | $\cosh^{-1}(x)$ |
| `acot` | $\cot^{-1}(x)$ |
| `asin` | $\sin^{-1}(x)$ |
| `asinh` | $\sinh^{-1}(x)$ |
| `atan` | $\tan^{-1}(x)$ |
| `avg` | $\overline X$ |
| `cos` | $\cos(x)$ |
| `cosh` | $\cosh(x)$ |
| `cot` | $\cot(x)$ |
| `exp` | $\exp(x)$ |
| `inf` | $\inf(X)$ |
| `lg` | $\lg(x)$ |
| `ln` | $\ln(x)$ |
| `log10` | $\log_{10}(x)$ |
| `log2` | $\log_2(x)$ |
| `max` | $\sup(X)$ |
| `min` | $\inf(X)$ |
| `prod` | $\displaystyle \prod_{i=0}^n x_i$ |
| `sgn` | $sgn(x)$ |
| `sign` | $sgn(x)$ |
| `sin` | $\sin(x)$ |
| `sinh` | $\sinh(x)$ |
| `sqrt` | $\sqrt{x}$ |
| `sum` | $\displaystyle\sum_{i=0}^n x_i$ |
| `sup` | $\sup(X)$ |
| `tan` | $\tan(x)$ |
| `tanh` | $\tanh(x)$ |

Operators: `+`, `-`, `*`, `/`, `^`, `%`

Braces: `()`, `[]`, `{}`

Floating points: `.`, `,`

Functions have only one argument, provided in braces. Operators must have two operands except minus (if it is the first character of equation or braced expression).

`avg`, `sum`, `max`, `sup`, `min`, `inf` and `prod` applied on `numpy.ndarray` produce `float`.

**! There is no error handling yet !**
