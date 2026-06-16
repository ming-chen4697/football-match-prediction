#!/usr/bin/env python
"""
Run all tests
"""

import sys
import pytest

if __name__ == "__main__":
    # Run pytest with verbose output
    exit_code = pytest.main(['-v', 'tests/'])
    sys.exit(exit_code)
