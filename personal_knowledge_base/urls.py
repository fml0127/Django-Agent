from django.urls import path, re_path

from . import views


urlpatterns = [
    # ── Auth ─────────────────────────────────────────────────────────────────
    path("auth/register", views.auth_register),
    path("auth/register-by-invite", views.auth_register),
    path("auth/invitations/lookup", lambda request: views.ok({"valid": False})),
    path("auth/login", views.auth_login),
    path("auth/auto-setup", views.auth_auto_setup),
    path("auth/config", views.auth_config),
    path("auth/switch-tenant", views.switch_tenant),
    path("auth/oidc/config", views.oidc_config),
    path("auth/oidc/url", views.oidc_url),
    path("auth/oidc/callback", views.oidc_callback),
    path("auth/refresh", views.auth_refresh),
    path("auth/validate", views.auth_validate),
    path("auth/logout", views.auth_logout),
    path("auth/me", views.auth_me),
    path("auth/me/preferences", views.auth_preferences),
    path("auth/change-password", views.auth_change_password),

    # ── Tenants ──────────────────────────────────────────────────────────────
    path("tenants", views.tenants_collection),
    path("tenants/all", views.tenants_collection),
    path("tenants/search", views.tenants_collection),
    path("tenants/kv/<str:key>", views.tenant_kv),
    path("tenants/<int:tenant_id>", views.tenant_detail),
    path("tenants/<int:tenant_id>/api-key", views.tenant_api_key),
    path("tenants/<int:tenant_id>/members", views.tenant_members),
    path("tenants/<int:tenant_id>/members/<str:user_id>", views.tenant_members),
    path("tenants/<int:tenant_id>/audit-log", views.audit_logs),

    # ── Knowledge Bases ──────────────────────────────────────────────────────
    path("knowledge-bases", views.knowledge_bases),
    path("knowledge-bases/copy", views.kb_copy),
    path("knowledge-bases/copy/progress/<str:task_id>", views.task_progress),
    path("knowledge-bases/<str:kb_id>", views.knowledge_bases),
    path("knowledge-bases/<str:kb_id>/pin", views.kb_pin),
    path("knowledge-bases/<str:kb_id>/hybrid-search", views.kb_hybrid_search),
    path("knowledge-bases/<str:kb_id>/move-targets", views.kb_move_targets),
    path("knowledge-bases/<str:kb_id>/knowledge/stats", views.knowledge_stats),
    path("knowledge-bases/<str:kb_id>/knowledge", views.knowledge_collection),
    path("knowledge-bases/<str:kb_id>/knowledge/batch-delete", views.knowledge_batch_delete),
    path("knowledge-bases/<str:kb_id>/knowledge/move", views.knowledge_move),
    path("knowledge-bases/<str:kb_id>/knowledge/file", views.knowledge_file),
    path("knowledge-bases/<str:kb_id>/tags", views.tags_collection),
    path("knowledge-bases/<str:kb_id>/tags/<str:tag_id>", views.tags_collection),

    # ── Knowledge ────────────────────────────────────────────────────────────
    path("knowledge/batch", views.knowledge_batch),
    path("knowledge/search", views.knowledge_search),
    path("knowledge/batch-delete", views.knowledge_batch_delete),
    path("knowledge/move", views.knowledge_move),
    path("knowledge/move/progress/<str:task_id>", views.task_progress),
    path("knowledge/<str:knowledge_id>", views.knowledge_detail),
    path("knowledge/<str:knowledge_id>/stages", views.knowledge_spans),
    path("knowledge/<str:knowledge_id>/spans", views.knowledge_spans),
    path("knowledge/<str:knowledge_id>/reparse", views.knowledge_reparse),
    path("knowledge/<str:knowledge_id>/cancel-parse", views.knowledge_cancel),
    path("knowledge/<str:knowledge_id>/download", views.knowledge_download),
    path("knowledge/<str:knowledge_id>/preview", views.knowledge_preview),

    # ── Chunks ───────────────────────────────────────────────────────────────
    path("chunks/<str:knowledge_id>", views.chunks_collection),
    path("chunks/<str:knowledge_id>/<str:chunk_id>", views.chunks_collection),
    path("chunks/by-id/<str:chunk_id>", views.chunks_collection),
    path("chunks/by-id/<str:chunk_id>/questions", views.chunks_collection),

    # ── Sessions ─────────────────────────────────────────────────────────────
    path("sessions", views.sessions_collection),
    path("sessions/batch", views.sessions_collection),
    path("sessions/<str:session_id>", views.sessions_collection),
    path("sessions/<str:session_id>/messages", views.session_messages_clear),
    path("sessions/<str:session_id>/generate_title", views.session_title),
    path("sessions/<str:session_id>/stop", views.session_stop),
    path("sessions/<str:session_id>/pin", views.session_pin),
    path("sessions/continue-stream/<str:session_id>", views.continue_stream),

    # ── Chat ─────────────────────────────────────────────────────────────────
    path("knowledge-chat/<str:session_id>", views.chat_endpoint),
    path("agent-chat/<str:session_id>", views.chat_endpoint, {"agent": True}),
    path("knowledge-search", views.knowledge_search_post),

    # ── Messages ─────────────────────────────────────────────────────────────
    path("messages/search", views.messages_search),
    path("messages/chat-history-stats", views.chat_history_stats),
    path("messages/<str:session_id>/load", views.messages_load),
    path("messages/<str:session_id>/<str:message_id>", views.message_delete),

    # ── Models ───────────────────────────────────────────────────────────────
    path("models/providers", views.model_providers),
    path("models/usage", views.model_usage),
    path("models", views.models_collection),
    path("models/<str:model_id>", views.models_collection),
    path("models/<str:model_id>/credentials", views.model_credentials),
    path("models/<str:model_id>/credentials/<str:field>", views.model_credentials),

    # ── Initialization ───────────────────────────────────────────────────────
    path("initialization/config/<str:kb_id>", views.initialization_config),
    path("initialization/initialize/<str:kb_id>", views.initialization_update),
    path("initialization/config/<str:kb_id>", views.initialization_update),

    # ── System ───────────────────────────────────────────────────────────────
    path("system/info", views.system_info),
    path("system/parser-engines", views.parser_engines),
    path("system/storage-engine-status", views.storage_status),
    path("system/admin/audit-log", views.audit_logs),

    # ── Wiki ─────────────────────────────────────────────────────────────────
    path("knowledge-bases/<str:kb_id>/wiki/pages", views.wiki_pages),
    re_path(r"^knowledge-bases/(?P<kb_id>[^/]+)/wiki/pages/(?P<slug>.*)$", views.wiki_pages),
    path("knowledge-bases/<str:kb_id>/wiki/folders", views.wiki_folders),
    path("knowledge-bases/<str:kb_id>/wiki/folders/<str:folder_id>", views.wiki_folders),
    path("knowledge-bases/<str:kb_id>/wiki/index", views.wiki_index),
    path("knowledge-bases/<str:kb_id>/wiki/log", views.wiki_log),
    path("knowledge-bases/<str:kb_id>/wiki/graph", views.wiki_graph),
    path("knowledge-bases/<str:kb_id>/wiki/stats", views.wiki_stats),
    path("knowledge-bases/<str:kb_id>/wiki/search", views.wiki_search),
    path("knowledge-bases/<str:kb_id>/wiki/lint", views.wiki_lint),
    path("knowledge-bases/<str:kb_id>/wiki/issues", views.wiki_issues),
    path("knowledge-bases/<str:kb_id>/wiki/issues/<str:issue_id>/status", views.wiki_issues),
    path("knowledgebase/<str:kb_id>/wiki/pages", views.wiki_pages),
    re_path(r"^knowledgebase/(?P<kb_id>[^/]+)/wiki/pages/(?P<slug>.*)$", views.wiki_pages),
    path("knowledgebase/<str:kb_id>/wiki/folders", views.wiki_folders),
    path("knowledgebase/<str:kb_id>/wiki/folders/<str:folder_id>", views.wiki_folders),
    path("knowledgebase/<str:kb_id>/wiki/index", views.wiki_index),
    path("knowledgebase/<str:kb_id>/wiki/log", views.wiki_log),
    path("knowledgebase/<str:kb_id>/wiki/graph", views.wiki_graph),
    path("knowledgebase/<str:kb_id>/wiki/stats", views.wiki_stats),
    path("knowledgebase/<str:kb_id>/wiki/search", views.wiki_search),
    path("knowledgebase/<str:kb_id>/wiki/lint", views.wiki_lint),
    path("knowledgebase/<str:kb_id>/wiki/issues", views.wiki_issues),
    path("knowledgebase/<str:kb_id>/wiki/issues/<str:issue_id>/status", views.wiki_issues),

    # ── Embed public ─────────────────────────────────────────────────────────
    path("embed/<str:channel_id>/exchange", views.embed_public, {"action": "exchange"}),
    path("embed/<str:channel_id>/config", views.embed_public, {"action": "config"}),
    path("embed/<str:channel_id>/suggested-questions", views.embed_public, {"action": "suggested-questions"}),
    path("embed/<str:channel_id>/chunks/<str:chunk_id>", views.embed_public, {"action": "chunks"}),
    path("embed/<str:channel_id>/sessions", views.embed_public, {"action": "sessions"}),
    path("embed/<str:channel_id>/knowledge-chat/<str:session_id>", views.embed_public, {"action": "knowledge-chat"}),
    path("embed/<str:channel_id>/agent-chat/<str:session_id>", views.embed_public, {"action": "agent-chat"}),
    path("embed/<str:channel_id>/messages/<str:session_id>/load", views.embed_public, {"action": "messages"}),
    path("embed/<str:channel_id>/sessions/<str:session_id>/stop", views.embed_public, {"action": "stop"}),
    path("embed/<str:channel_id>/sessions/<str:session_id>/events", views.embed_public, {"action": "events"}),
]
