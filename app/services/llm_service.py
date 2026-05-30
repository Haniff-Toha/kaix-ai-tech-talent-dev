"""
LLM service with automatic failover.

Wraps LangChain ChatOpenAI instances and provides:
    - Primary → fallback failover for reasoning LLM
    - Structured output parsing via LangChain
    - Consistent error handling and logging
"""

import logging
from typing import Any

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage

logger = logging.getLogger(__name__)


class LLMService:
    """
    Unified LLM access with automatic failover.

    Usage:
        reasoning = LLMService(primary=reasoning_llm, fallback=reasoning_fallback_llm)
        result = await reasoning.ainvoke(messages)
    """

    def __init__(
        self,
        primary: BaseChatModel,
        fallback: BaseChatModel | None = None,
        name: str = "default",
    ):
        self.primary = primary
        self.fallback = fallback
        self.name = name

    async def ainvoke(
        self,
        messages: list[BaseMessage] | Any,
        **kwargs,
    ) -> Any:
        """Invoke the primary LLM, falling back if it fails."""
        try:
            return await self.primary.ainvoke(messages, **kwargs)
        except Exception as e:
            logger.warning(
                f"[{self.name}] Primary LLM failed: {type(e).__name__}: {e}"
            )
            if self.fallback:
                logger.info(f"[{self.name}] Falling back to secondary LLM")
                return await self.fallback.ainvoke(messages, **kwargs)
            raise

    async def ainvoke_with_structured_output(
        self,
        messages: list[BaseMessage] | Any,
        schema: type,
        **kwargs,
    ) -> Any:
        """
        Invoke with structured output parsing.
        Uses LangChain's with_structured_output for JSON schema enforcement.
        """
        structured_primary = self.primary.with_structured_output(schema)
        try:
            return await structured_primary.ainvoke(messages, **kwargs)
        except Exception as e:
            logger.warning(
                f"[{self.name}] Primary structured output failed: {type(e).__name__}: {e}"
            )
            if self.fallback:
                logger.info(f"[{self.name}] Falling back to secondary LLM (structured)")
                structured_fallback = self.fallback.with_structured_output(schema)
                return await structured_fallback.ainvoke(messages, **kwargs)
            raise

    async def astream(
        self,
        messages: list[BaseMessage] | Any,
        **kwargs,
    ):
        """Stream from the primary LLM, falling back if it fails."""
        try:
            async for chunk in self.primary.astream(messages, **kwargs):
                yield chunk
        except Exception as e:
            logger.warning(
                f"[{self.name}] Primary LLM stream failed: {type(e).__name__}: {e}"
            )
            if self.fallback:
                logger.info(f"[{self.name}] Falling back to secondary LLM (stream)")
                async for chunk in self.fallback.astream(messages, **kwargs):
                    yield chunk
            else:
                raise
