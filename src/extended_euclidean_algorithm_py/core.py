"""Extended Euclidean Algorithm for two integers."""

from __future__ import annotations

from typing import NamedTuple


class ExtendedGcdResult(NamedTuple):
    """Result of :func:`extended_gcd`.

    Holds the gcd and the Bézout coefficients ``x`` and ``y`` such that
    ``a*x + b*y == gcd``.  The sign of the coefficients is governed by the
    algorithm's invariant below, so callers that care only about existence
    of the identity should ignore the signs and use ``gcd``.
    """

    gcd: int
    x: int
    y: int


def extended_gcd(a: int, b: int) -> ExtendedGcdResult:
    """Return ``(gcd, x, y)`` with ``a*x + b*y == gcd``.

    Uses the iterative Extended Euclidean Algorithm rather than the textbook
    recursive form: it avoids Python recursion limits on very large inputs and
    keeps a fixed memory footprint regardless of the input size.

    Sign convention
    ---------------
    ``x`` carries the sign of ``a`` and ``y`` carries the sign of ``b``, so
    the Bézout identity always holds with *addition*.  The gcd itself is
    always non-negative.  This is the single point where two reasonable
    conventions diverge (``gcd(a,b)`` vs ``gcd(|a|,|b|)``); we chose the
    identity-preserving convention because it is the one callers need for
    modular inverses and Diophantine solving.

    Edge cases
    ----------
    * ``extended_gcd(0, 0) == (0, 0, 0)``.  The gcd of two zeros is
      conventionally 0, and any pair of coefficients satisfies the identity
      trivially; we return zeros for determinism.
    * A single zero input yields ``|non-zero|`` as the gcd, with the
      coefficient of the zero input set to 0 and the coefficient of the
      non-zero input carrying its sign.
    """
    if not isinstance(a, int) or isinstance(a, bool):
        raise TypeError(f"a must be int, got {type(a).__name__}")
    if not isinstance(b, int) or isinstance(b, bool):
        raise TypeError(f"b must be int, got {type(b).__name__}")

    if a == 0 and b == 0:
        return ExtendedGcdResult(0, 0, 0)

    # Work with signs preserved so the final coefficients line up with the
    # original inputs.  The loop invariant is  a*old_r + b*0 == old_r  and
    #  a*old_s + b*old_t == old_s  (and symmetrically for the "new" row),
    # which we maintain by carrying the sign through every step rather than
    # by normalising up front.
    old_r, new_r = a, b
    old_s, new_s = 1, 0
    old_t, new_t = 0, 1

    while new_r != 0:
        quotient = old_r // new_r
        old_r, new_r = new_r, old_r - quotient * new_r
        old_s, new_s = new_s, old_s - quotient * new_s
        old_t, new_t = new_t, old_t - quotient * new_t

    # ``old_r`` is now the gcd, but it may be negative when ``a < 0`` and
    # ``b == 0``.  The sign of the gcd is decoupled from the signs of the
    # coefficients in the identity, so flip both into the identity without
    # changing its truth.
    gcd = old_r if old_r >= 0 else -old_r
    x = old_s
    y = old_t
    if old_r < 0:
        x, y = -x, -y

    return ExtendedGcdResult(gcd, x, y)
