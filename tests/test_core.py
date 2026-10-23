"""Tests for extended_euclidean_algorithm_py.core."""

import unittest

from extended_euclidean_algorithm_py.core import extended_gcd, ExtendedGcdResult


class ExtendedGcdTests(unittest.TestCase):
    def _check_identity(self, a, b):
        """Verify a*x + b*y == gcd and gcd >= 0 for the given inputs."""
        result = extended_gcd(a, b)
        self.assertIsInstance(result, ExtendedGcdResult)
        self.assertIsInstance(result.gcd, int)
        self.assertIsInstance(result.x, int)
        self.assertIsInstance(result.y, int)
        self.assertGreaterEqual(result.gcd, 0)
        self.assertEqual(a * result.x + b * result.y, result.gcd)
        return result

    def test_coprime_pair(self):
        # 99 and 78: classic example, gcd 3.
        result = extended_gcd(99, 78)
        self.assertEqual(result.gcd, 3)
        self.assertEqual(99 * result.x + 78 * result.y, 3)

    def test_equal_pair(self):
        result = extended_gcd(12, 12)
        self.assertEqual(result.gcd, 12)
        self._check_identity(12, 12)

    def test_one_divides_other(self):
        result = extended_gcd(7, 21)
        self.assertEqual(result.gcd, 7)
        self._check_identity(7, 21)

    def test_first_divides_second_negative(self):
        result = extended_gcd(7, -21)
        self.assertEqual(result.gcd, 7)
        self._check_identity(7, -21)

    def test_coprime_returns_one(self):
        result = extended_gcd(8, 15)
        self.assertEqual(result.gcd, 1)
        self._check_identity(8, 15)

    def test_one_of_pair_is_zero(self):
        # gcd(0, 5) == 5 and the identity collapses to 5*y == 5.
        result = extended_gcd(0, 5)
        self.assertEqual(result.gcd, 5)
        self.assertEqual(result.x, 0)
        self.assertEqual(result.y, 1)
        self._check_identity(0, 5)

    def test_non_zero_first_with_zero_second(self):
        # gcd(5, 0) == 5 and the identity collapses to 5*x == 5.
        result = extended_gcd(5, 0)
        self.assertEqual(result.gcd, 5)
        self.assertEqual(result.x, 1)
        self.assertEqual(result.y, 0)
        self._check_identity(5, 0)

    def test_negative_non_zero_first_with_zero_second(self):
        # x carries the sign of a, so the identity uses addition: (-5)*(-1) + 0*0 == 5.
        result = extended_gcd(-5, 0)
        self.assertEqual(result.gcd, 5)
        self.assertEqual(result.x, -1)
        self.assertEqual(result.y, 0)
        self._check_identity(-5, 0)

    def test_both_zero(self):
        result = extended_gcd(0, 0)
        self.assertEqual(result, (0, 0, 0))

    def test_both_negative(self):
        result = extended_gcd(-48, -18)
        self.assertEqual(result.gcd, 6)
        self._check_identity(-48, -18)

    def test_first_negative(self):
        result = extended_gcd(-48, 18)
        self.assertEqual(result.gcd, 6)
        self._check_identity(-48, 18)

    def test_second_negative(self):
        result = extended_gcd(48, -18)
        self.assertEqual(result.gcd, 6)
        self._check_identity(48, -18)

    def test_large_inputs_identity_holds(self):
        a, b = 1071 * 10**40, 462 * 10**40
        result = extended_gcd(a, b)
        self.assertEqual(result.gcd, 21 * 10**40)
        self._check_identity(a, b)

    def test_bool_rejected(self):
        # bool is a subclass of int; rejecting it prevents silent surprises.
        with self.assertRaises(TypeError):
            extended_gcd(True, 5)
        with self.assertRaises(TypeError):
            extended_gcd(5, False)

    def test_non_int_rejected(self):
        with self.assertRaises(TypeError):
            extended_gcd(1.0, 5)
        with self.assertRaises(TypeError):
            extended_gcd(5, "3")


if __name__ == "__main__":
    unittest.main()
