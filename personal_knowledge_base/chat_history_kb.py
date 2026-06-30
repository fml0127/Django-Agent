"""
ChatHistoryKB：对话历史知识库

参考 WeKnora 的 ChatHistoryKB 设计：
- 将对话历史索引到专用知识库
- 支持 keyword/vector/hybrid 三种搜索模式
- 可用于检索历史对话中的相关信息

注意：这是一个可选功能，需要在 Tenant 配置中启用。
"""

import logging
import threading
from typing import Optional

logger = logging.getLogger(__name__)

# ChatHistoryKB 配置键
CHAT_HISTORY_KB_CONFIG_KEY = "chat_history_config"

# 默认配置
DEFAULT_CONFIG = {
    "enabled": False,
    "embedding_model_id": "",
    "knowledge_base_id": "",
}


def get_chat_history_config(tenant) -> dict:
    """获取租户的 ChatHistoryKB 配置。"""
    config = tenant.chat_history_config or {}
    return {**DEFAULT_CONFIG, **config}


def is_chat_history_enabled(tenant) -> bool:
    """检查 ChatHistoryKB 是否启用。"""
    config = get_chat_history_config(tenant)
    return config.get("enabled", False)


def get_or_create_chat_history_kb(tenant) -> Optional[str]:
    """
    获取或创建 ChatHistoryKB。
    返回 KnowledgeBase ID。
    """
    from .models import KnowledgeBase

    config = get_chat_history_config(tenant)
    kb_id = config.get("knowledge_base_id", "")

    if kb_id:
        kb = KnowledgeBase.objects.filter(id=kb_id, tenant=tenant, deleted_at__isnull=True).first()
        if kb:
            return kb_id

    # 创建新的 ChatHistoryKB
    kb = KnowledgeBase.objects.create(
        tenant=tenant,
        name="__chat_history__",
        description="System-managed knowledge base for chat history indexing",
        type="document",
        is_temporary=False,
    )

    # 更新配置
    config["knowledge_base_id"] = str(kb.id)
    tenant.chat_history_config = config
    tenant.save(update_fields=["chat_history_config", "updated_at"])

    logger.info(f"[ChatHistoryKB] Created chat history KB: {kb.id}")
    return str(kb.id)


def index_message_to_kb_async(tenant, message):
    """
    异步将消息索引到 ChatHistoryKB。
    参考 WeKnora 的 IndexMessageToKB。
    """
    if not is_chat_history_enabled(tenant):
        return

    def _index():
        try:
            _index_message(tenant, message)
        except Exception as e:
            logger.exception(f"[ChatHistoryKB] Failed to index message: {e}")

    thread = threading.Thread(target=_index, daemon=True)
    thread.start()


def _index_message(tenant, message):
    """
    将消息索引到 ChatHistoryKB。
    创建一个 Knowledge 记录，内容为消息内容。
    """
    from .models import Knowledge, KnowledgeBase, Chunk

    kb_id = get_or_create_chat_history_kb(tenant)
    if not kb_id:
        return

    kb = KnowledgeBase.objects.filter(id=kb_id, tenant=tenant).first()
    if not kb:
        return

    # 检查是否已索引
    existing = Knowledge.objects.filter(
        tenant=tenant,
        knowledge_base=kb,
        metadata__message_id=str(message.id),
    ).first()
    if existing:
        return

    # 创建 Knowledge 记录
    content = message.content or ""
    if not content.strip():
        return

    knowledge = Knowledge.objects.create(
        tenant=tenant,
        knowledge_base=kb,
        type="file",
        title=f"Chat message {message.id[:8]}",
        description=f"Session: {message.session_id}, Role: {message.role}",
        source="chat_history",
        parse_status="completed",
        file_name=f"chat_{message.id[:8]}.txt",
        file_type="txt",
        metadata={
            "message_id": str(message.id),
            "session_id": str(message.session_id),
            "role": message.role,
            "request_id": message.request_id,
            "created_at": message.created_at.isoformat() if message.created_at else "",
        },
    )

    # 创建 Chunk
    Chunk.objects.create(
        tenant=tenant,
        knowledge_base=kb,
        knowledge=knowledge,
        content=content,
        chunk_index=0,
        is_enabled=True,
    )

    logger.debug(f"[ChatHistoryKB] Indexed message {message.id[:8]}")


def search_chat_history(tenant, query: str, limit: int = 5) -> list[dict]:
    """
    搜索 ChatHistoryKB 中的历史对话。
    参考 WeKnora 的 MessageSearchParams。
    """
    from .models import Chunk, KnowledgeBase
    from .search import hybrid_search

    config = get_chat_history_config(tenant)
    kb_id = config.get("knowledge_base_id", "")

    if not kb_id:
        return []

    # 使用现有的 hybrid_search 搜索
    try:
        results = hybrid_search(tenant.id, [kb_id], query, limit)
        return results
    except Exception as e:
        logger.warning(f"[ChatHistoryKB] Search failed: {e}")
        return []
