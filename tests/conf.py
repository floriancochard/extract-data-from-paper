import pytest
from .test_type import Equality


def pytest_assertrepr_compare(op, left, right):
    """Custom assertion representation for Equality class comparisons."""
    if isinstance(left, Equality) and isinstance(right, Equality) and op == "==":
        return [
            "Comparing Equality instances",
            "   vals: {} != {}".format(left.val, right.val)
        ]
