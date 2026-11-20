# extended_euclidean_algorithm_py

Returns the Bézout coefficients and greatest common divisor of two integers, suitable for modular inverses and Diophantine equation solving.

```python
from extended_euclidean_algorithm_py import extended_gcd, ExtendedGcdResult

result = extended_gcd(99, 78)
# ExtendedGcdResult(gcd=3, x=-11, y=14)
assert 99 * result.x + 78 * result.y == result.gcd
```

## Why this exists

The identity `a*x + b*y == gcd(a, b)` is the backbone of modular inverse computation and linear Diophantine solving, but a naive recursive implementation blows Python's recursion limit on large inputs. This library implements the iterative form, which uses constant space and avoids any recursion limit, with no third-party dependencies.

The one design decision worth flagging: we preserve the signs of the inputs in the coefficients so the Bézout identity holds with *addition* (`a*x + b*y == gcd`), and we return a non-negative gcd in every case. That means `extended_gcd(-5, 0)` returns `(gcd=5, x=-1, y=0)` rather than `(gcd=-5, x=1, y=0)`. If you need the signed-gcd convention, negate both coefficients yourself.

The awkward edge: `extended_gcd(0, 0)` returns `(0, 0, 0)`. Every pair of coefficients trivially satisfies `0*x + 0*y == 0`, so we return zeros for determinism rather than picking an arbitrary non-trivial pair.

## Design notes

The window stores values eagerly rather than keeping running aggregates. Running
sums drift with floating point over long streams, and recomputing from a small
buffer is cheap enough that the drift is not worth the speed.

## Limitations

Values are coerced to floats, so very large integers lose precision. If you need
exact integer aggregates over a window, this is the wrong tool.

