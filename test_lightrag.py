"""
Comprehensive tests for LightRAG functionality.
"""

import pytest
import asyncio
from unittest.mock import Mock, patch
from lightrag import LightRAG, QueryParam
from lightrag.utils import EmbeddingFunc, compute_mdhash_id


class TestEmbeddingFunc:
    """Mock embedding function for testing."""

    def __init__(self):
        self.embedding_dim = 384
        self.max_token_size = 8192

    async def __call__(self, text: str) -> list[float]:
        # Simple mock embedding - return dummy values
        return [0.0] * self.embedding_dim


class TestLightRAGInit:
    """Test LightRAG initialization."""

    def test_basic_init(self):
        """Test basic initialization with minimal parameters."""
        embedding_func = TestEmbeddingFunc()
        rag = LightRAG(
            working_dir="./test_output",
            llm_model_func=Mock(),
            embedding_func=embedding_func,
        )
        assert rag.working_dir == "./test_output"
        assert rag.embedding_func == embedding_func

    def test_init_with_all_params(self):
        """Test initialization with all parameters."""
        embedding_func = TestEmbeddingFunc()
        rag = LightRAG(
            working_dir="./test_output",
            llm_model_func=Mock(),
            embedding_func=embedding_func,
            llm_model_name="test-model",
            embedding_model_name="test-embedding",
            chunk_token_size=1000,
            chunk_overlap_token_size=100,
            tiktoken_model_name="gpt-3.5-turbo",
        )
        assert rag.chunk_token_size == 1000
        assert rag.chunk_overlap_token_size == 100
        assert rag.tiktoken_model_name == "gpt-3.5-turbo"


class TestQueryParams:
    """Test QueryParam functionality."""

    def test_default_params(self):
        """Test default parameter initialization."""
        param = QueryParam()
        assert param.mode == "local"
        assert param.top_k == 5
        assert param.max_token_for_text_unit == 4000
        assert param.max_token_for_global_context == 4000
        assert param.max_token_for_relation_extract == 2000

    def test_custom_params(self):
        """Test custom parameter initialization."""
        param = QueryParam(mode="global", top_k=10, max_token_for_text_unit=8000)
        assert param.mode == "global"
        assert param.top_k == 10
        assert param.max_token_for_text_unit == 8000


class TestEmbedding:
    """Test embedding functionality."""

    @pytest.fixture
    def embedding_func(self):
        return TestEmbeddingFunc()

    @pytest.mark.asyncio
    async def test_embedding_call(self, embedding_func):
        """Test embedding function call."""
        result = await embedding_func("test text")
        assert isinstance(result, list)
        assert len(result) == 384
        assert all(isinstance(x, float) for x in result)

    def test_embedding_properties(self, embedding_func):
        """Test embedding function properties."""
        assert embedding_func.embedding_dim == 384
        assert embedding_func.max_token_size == 8192


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


class TestWorkflow:
    """Test end-to-end workflows."""

    @pytest.fixture
    def mock_rag(self):
        embedding_func = TestEmbeddingFunc()
        return LightRAG(
            working_dir="./test_workflow",
            llm_model_func=Mock(return_value="test response"),
            embedding_func=embedding_func,
        )

    def test_insert_workflow(self, mock_rag):
        """Test document insertion workflow."""
        # Mock the async insertion
        with patch.object(mock_rag, "ainsert", return_value=None) as mock_ainsert:
            result = mock_rag.insert("test document")
            mock_ainsert.assert_called_once_with("test document")

    def test_query_workflow(self, mock_rag):
        """Test query workflow."""
        # Mock the async query
        with patch.object(
            mock_rag, "aquery", return_value="test response"
        ) as mock_aquery:
            result = mock_rag.query("test query")
            mock_aquery.assert_called_once()
            assert result == "test response"


class TestErrorHandling:
    """Test error handling scenarios."""

    def test_invalid_working_dir(self):
        """Test handling of invalid working directory."""
        with pytest.raises(Exception):
            LightRAG(
                working_dir="",  # Invalid empty directory
                llm_model_func=Mock(),
                embedding_func=TestEmbeddingFunc(),
            )

    def test_none_embedding_func(self):
        """Test handling of None embedding function."""
        with pytest.raises(Exception):
            LightRAG(
                working_dir="./test",
                llm_model_func=Mock(),
                embedding_func=None,  # Invalid None
            )


class TestConfiguration:
    """Test configuration management."""

    def test_default_configuration(self):
        """Test default configuration values."""
        rag = LightRAG(
            working_dir="./test",
            llm_model_func=Mock(),
            embedding_func=TestEmbeddingFunc(),
        )
        assert hasattr(rag, "llm_model_func")
        assert hasattr(rag, "embedding_func")
        assert rag.chunk_token_size > 0

    def test_configuration_override(self):
        """Test configuration value overrides."""
        custom_size = 2000
        rag = LightRAG(
            working_dir="./test",
            llm_model_func=Mock(),
            embedding_func=TestEmbeddingFunc(),
            chunk_token_size=custom_size,
        )
        assert rag.chunk_token_size == custom_size


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
