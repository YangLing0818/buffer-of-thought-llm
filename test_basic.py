"""
Basic tests for LightRAG core functionality.
"""

import pytest
from lightrag.utils import compute_mdhash_id


class TestUtils:
    """Test utility functions."""

    def test_compute_mdhash_id(self):
        """Test MD5 hash computation."""
        text = "test input"
        hash_id = compute_mdhash_id(text)
        assert isinstance(hash_id, str)
        assert len(hash_id) == 32  # MD5 hash length
        assert hash_id.startswith("doc-")

    def test_compute_mdhash_id_with_prefix(self):
        """Test MD5 hash with custom prefix."""
        text = "test input"
        hash_id = compute_mdhash_id(text, prefix="custom-")
        assert hash_id.startswith("custom-")
        assert len(hash_id) == 32 + 7  # prefix + MD5 hash

    def test_compute_mdhash_id_consistency(self):
        """Test MD5 hash consistency."""
        text = "test input"
        hash1 = compute_mdhash_id(text)
        hash2 = compute_mdhash_id(text)
        assert hash1 == hash2


class TestQueryParams:
    """Test QueryParam functionality."""

    from lightrag import QueryParam

    def test_default_params(self):
        """Test default parameter initialization."""
        param = self.QueryParam()
        assert param.mode == "local"
        assert param.top_k == 5
        assert param.max_token_for_text_unit == 4000
        assert param.max_token_for_global_context == 4000
        assert param.max_token_for_relation_extract == 2000

    def test_custom_params(self):
        """Test custom parameter initialization."""
        param = self.QueryParam(mode="global", top_k=10, max_token_for_text_unit=8000)
        assert param.mode == "global"
        assert param.top_k == 10
        assert param.max_token_for_text_unit == 8000


class TestEmbeddingFunc:
    """Test EmbeddingFunc dataclass."""

    from lightrag.utils import EmbeddingFunc

    def test_embedding_func_creation(self):
        """Test EmbeddingFunc can be created with required fields."""

        def mock_func(text):
            return [0.0] * 384

        embedding_func = self.EmbeddingFunc(
            embedding_dim=384, max_token_size=8192, func=mock_func
        )

        assert embedding_func.embedding_dim == 384
        assert embedding_func.max_token_size == 8192
        assert embedding_func.func == mock_func


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
