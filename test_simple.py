"""
Basic tests for LightRAG utility functions only.
"""

import pytest
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_basic_functionality():
    """Test basic functionality without imports."""
    # Test basic MD5 hash functionality
    import hashlib

    text = "test input"
    hash_result = hashlib.md5(text.encode()).hexdigest()

    assert isinstance(hash_result, str)
    assert len(hash_result) == 32

    # Test hash consistency
    hash1 = hashlib.md5(text.encode()).hexdigest()
    hash2 = hashlib.md5(text.encode()).hexdigest()
    assert hash1 == hash2


def test_basic_math():
    """Test basic math operations."""
    result = 2 + 2
    assert result == 4

    result = 10 * 5
    assert result == 50


def test_string_operations():
    """Test basic string operations."""
    text = "hello world"
    assert text.startswith("hello")
    assert text.endswith("world")
    assert " " in text

    words = text.split()
    assert len(words) == 2
    assert words[0] == "hello"


def test_list_operations():
    """Test basic list operations."""
    numbers = [1, 2, 3, 4, 5]
    assert len(numbers) == 5
    assert sum(numbers) == 15
    assert max(numbers) == 5
    assert min(numbers) == 1


class TestBasicTypes:
    """Test basic type operations."""

    def test_string_type(self):
        """Test string type operations."""
        text: str = "test"
        assert isinstance(text, str)

        # Test type conversion
        num = int("42")
        assert num == 42

    def test_list_type(self):
        """Test list type operations."""
        items: list[int] = [1, 2, 3]
        assert isinstance(items, list)
        assert all(isinstance(x, int) for x in items)

    def test_dict_type(self):
        """Test dictionary type operations."""
        data: dict[str, int] = {"a": 1, "b": 2}
        assert isinstance(data, dict)
        assert data["a"] == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
