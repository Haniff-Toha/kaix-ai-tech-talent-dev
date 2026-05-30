"""
Embedding service using Google Gemini.

Wraps the google-genai SDK directly (not langchain) to support
output_dimensionality for reduced dimensions (768 instead of 3072).

Supabase pgvector has a 2000 dimension limit, so we use 768 dims.
Gemini embedding-2-preview uses Matryoshka Representation Learning (MRL),
so reduced dimensions maintain excellent quality.
"""

import logging
import math

from google import genai
from google.genai import types

from app.config import settings

logger = logging.getLogger(__name__)


def _truncate_and_normalize(vector: list[float], dim: int) -> list[float]:
    """
    Truncate a vector to `dim` dimensions and L2-normalize it.
    Safe for MRL-trained models like Gemini embedding-2-preview.
    """
    truncated = vector[:dim]
    norm = math.sqrt(sum(x * x for x in truncated))
    if norm > 0:
        return [x / norm for x in truncated]
    return truncated


class EmbeddingService:
    """
    Gemini embedding wrapper with dimension control.

    Uses gemini-embedding-2-preview with:
        - output_dimensionality=768 (fits pgvector 2000 limit)
        - task_type hints for better retrieval quality
        - fallback truncation if API doesn't honor dimensionality
    """

    def __init__(self):
        self.client = genai.Client(api_key=settings.gemini_api_key)
        self.model = f"models/{settings.gemini_embedding_model}"
        self.dimensions = settings.embedding_dimension

    async def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Embed a batch of document texts for storage."""
        try:
            result = self.client.models.embed_content(
                model=self.model,
                contents=texts,
                config=types.EmbedContentConfig(
                    task_type="RETRIEVAL_DOCUMENT",
                    output_dimensionality=self.dimensions,
                ),
            )
            embeddings = [e.values for e in result.embeddings]

            # Fallback: truncate if API returned more dims than expected
            if embeddings and len(embeddings[0]) > self.dimensions:
                logger.info(
                    f"Truncating embeddings from {len(embeddings[0])} to {self.dimensions} dims"
                )
                embeddings = [
                    _truncate_and_normalize(e, self.dimensions) for e in embeddings
                ]

            return embeddings
        except Exception as e:
            logger.error(f"Document embedding failed: {e}")
            raise

    async def embed_query(self, text: str) -> list[float]:
        """Embed a single query text for similarity search."""
        try:
            result = self.client.models.embed_content(
                model=self.model,
                contents=text,
                config=types.EmbedContentConfig(
                    task_type="RETRIEVAL_QUERY",
                    output_dimensionality=self.dimensions,
                ),
            )
            embedding = result.embeddings[0].values

            # Fallback: truncate if API returned more dims than expected
            if len(embedding) > self.dimensions:
                embedding = _truncate_and_normalize(embedding, self.dimensions)

            return embedding
        except Exception as e:
            logger.error(f"Query embedding failed: {e}")
            raise


# Singleton instance
embedding_service = EmbeddingService()
