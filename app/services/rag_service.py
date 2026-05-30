"""
RAG service — pgvector similarity search and chunk management.

Handles both Knowledge RAG (shared career content) and User RAG (personal history).
"""

import logging
import uuid

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import KnowledgeRAGChunk, UserRAGChunk
from app.services.embedding_service import embedding_service

logger = logging.getLogger(__name__)


class RAGService:
    """
    Retrieval-Augmented Generation service using pgvector.

    Methods:
        - query_knowledge_rag: search career knowledge base
        - query_user_rag: search user's personal history
        - store_knowledge_chunk: add career content chunk
        - store_user_chunk: add user activity/note chunk
    """

    async def query_knowledge_rag(
        self,
        db: AsyncSession,
        query: str,
        career_track: str | None = None,
        top_k: int = 8,
    ) -> list[dict]:
        """
        Search Knowledge RAG for career-relevant content.

        Args:
            query: natural language query
            career_track: optional filter by track (e.g. 'backend_engineer')
            top_k: number of results
        """
        query_embedding = await embedding_service.embed_query(query)

        # Build query with optional career_track filter
        # NOTE: Use CAST(:param AS vector) instead of :param::vector
        # because asyncpg interprets :: as a parameter separator
        filter_clause = ""
        params = {"embedding": str(query_embedding), "limit": top_k}
        if career_track:
            filter_clause = "AND career_track = :career_track"
            params["career_track"] = career_track

        sql = text(f"""
            SELECT id, content, metadata, career_track,
                   1 - (embedding <=> CAST(:embedding AS vector)) AS similarity
            FROM knowledge_rag
            WHERE embedding IS NOT NULL
            {filter_clause}
            ORDER BY embedding <=> CAST(:embedding AS vector)
            LIMIT :limit
        """)

        result = await db.execute(sql, params)
        rows = result.fetchall()

        logger.info(f"Knowledge RAG query returned {len(rows)} results (track={career_track})")

        return [
            {
                "id": str(row.id),
                "content": row.content,
                "metadata": row.metadata,
                "career_track": row.career_track,
                "similarity": round(row.similarity, 4),
            }
            for row in rows
        ]

    async def query_user_rag(
        self,
        db: AsyncSession,
        user_id: uuid.UUID,
        query: str,
        top_k: int = 5,
    ) -> list[dict]:
        """Search user's personal RAG for activity history context."""
        query_embedding = await embedding_service.embed_query(query)

        sql = text("""
            SELECT id, content, metadata,
                   1 - (embedding <=> CAST(:embedding AS vector)) AS similarity
            FROM user_rag
            WHERE user_id = :user_id
              AND embedding IS NOT NULL
            ORDER BY embedding <=> CAST(:embedding AS vector)
            LIMIT :limit
        """)

        result = await db.execute(sql, {
            "embedding": str(query_embedding),
            "user_id": str(user_id),
            "limit": top_k,
        })
        rows = result.fetchall()

        return [
            {
                "id": str(row.id),
                "content": row.content,
                "metadata": row.metadata,
                "similarity": round(row.similarity, 4),
            }
            for row in rows
        ]

    async def store_knowledge_chunk(
        self,
        db: AsyncSession,
        content: str,
        metadata: dict,
        career_track: str,
    ) -> KnowledgeRAGChunk:
        """Embed and store a Knowledge RAG chunk."""
        embedding = (await embedding_service.embed_documents([content]))[0]

        chunk = KnowledgeRAGChunk(
            content=content,
            embedding=embedding,
            metadata_=metadata,
            career_track=career_track,
        )
        db.add(chunk)
        await db.flush()
        logger.info(f"Stored knowledge chunk for track={career_track}: {content[:60]}...")
        return chunk

    async def store_user_chunk(
        self,
        db: AsyncSession,
        user_id: uuid.UUID,
        content: str,
        metadata: dict,
    ) -> UserRAGChunk:
        """Embed and store a User RAG chunk."""
        embedding = (await embedding_service.embed_documents([content]))[0]

        chunk = UserRAGChunk(
            user_id=user_id,
            content=content,
            embedding=embedding,
            metadata_=metadata,
        )
        db.add(chunk)
        await db.flush()
        logger.info(f"Stored user chunk for user={user_id}: {content[:60]}...")
        return chunk


# Singleton instance
rag_service = RAGService()
