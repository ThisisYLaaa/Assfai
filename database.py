import sqlite3
import json
import uuid
from datetime import datetime

from module_lg import get_logger

logger = get_logger("数据库")

DB_PATH = "chat_history.db"

def _get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    conn = _get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL DEFAULT '新会话',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            operation_stack TEXT DEFAULT '[]'
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL DEFAULT '',
            tool_calls TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(session_id) REFERENCES sessions(id) ON DELETE CASCADE
        )
    """)
    conn.commit()
    conn.close()
    logger.info("数据库初始化完成")

def create_session(title="新会话"):
    session_id = str(uuid.uuid4())
    conn = _get_conn()
    conn.execute(
        "INSERT INTO sessions (id, title, created_at, updated_at) VALUES (?, ?, ?, ?)",
        (session_id, title, datetime.now(), datetime.now())
    )
    conn.commit()
    conn.close()
    logger.info(f"创建会话: {session_id} ({title})")
    return {
        "id": session_id,
        "title": title,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }

def get_sessions():
    conn = _get_conn()
    rows = conn.execute(
        "SELECT id, title, created_at, updated_at FROM sessions ORDER BY updated_at DESC"
    ).fetchall()
    sessions = []
    for row in rows:
        cnt_row = conn.execute(
            "SELECT COUNT(*) as cnt FROM messages WHERE session_id = ?", (row["id"],)
        ).fetchone()
        sessions.append({
            "id": row["id"],
            "title": row["title"],
            "created_at": row["created_at"],
            "updated_at": row["updated_at"],
            "message_count": cnt_row["cnt"] if cnt_row else 0
        })
    conn.close()
    return sessions

def update_session_title(session_id, title):
    conn = _get_conn()
    conn.execute(
        "UPDATE sessions SET title = ?, updated_at = ? WHERE id = ?",
        (title, datetime.now(), session_id)
    )
    conn.commit()
    conn.close()
    logger.info(f"更新会话标题: {session_id} -> {title}")
    return {"id": session_id, "title": title}

def delete_session(session_id):
    conn = _get_conn()
    conn.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
    conn.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
    conn.commit()
    conn.close()
    logger.info(f"删除会话: {session_id}")

def add_message(session_id, role, content, tool_calls=None):
    conn = _get_conn()
    tool_calls_json = json.dumps(tool_calls, ensure_ascii=False) if tool_calls else None
    conn.execute(
        "INSERT INTO messages (session_id, role, content, tool_calls, timestamp) VALUES (?, ?, ?, ?, ?)",
        (session_id, role, content or "", tool_calls_json, datetime.now())
    )
    conn.execute(
        "UPDATE sessions SET updated_at = ? WHERE id = ?",
        (datetime.now(), session_id)
    )
    conn.commit()
    conn.close()

def get_messages(session_id):
    conn = _get_conn()
    rows = conn.execute(
        "SELECT id, session_id, role, content, tool_calls, timestamp FROM messages WHERE session_id = ? ORDER BY id ASC",
        (session_id,)
    ).fetchall()
    conn.close()
    messages = []
    for row in rows:
        msg = {
            "id": row["id"],
            "session_id": row["session_id"],
            "role": row["role"],
            "content": row["content"],
            "timestamp": row["timestamp"]
        }
        if row["tool_calls"]:
            try:
                msg["tool_calls"] = json.loads(row["tool_calls"])
            except json.JSONDecodeError:
                msg["tool_calls"] = None
        else:
            msg["tool_calls"] = None
        messages.append(msg)
    return messages

def push_operation(session_id, undo_data):
    conn = _get_conn()
    row = conn.execute(
        "SELECT operation_stack FROM sessions WHERE id = ?", (session_id,)
    ).fetchone()
    if not row:
        conn.close()
        return
    stack = json.loads(row["operation_stack"])
    stack.append(undo_data)
    conn.execute(
        "UPDATE sessions SET operation_stack = ?, updated_at = ? WHERE id = ?",
        (json.dumps(stack, ensure_ascii=False), datetime.now(), session_id)
    )
    conn.commit()
    conn.close()
    logger.info(f"推送撤回操作到会话 {session_id}: {undo_data.get('method', 'unknown')}")

def pop_operation(session_id):
    conn = _get_conn()
    row = conn.execute(
        "SELECT operation_stack FROM sessions WHERE id = ?", (session_id,)
    ).fetchone()
    if not row:
        conn.close()
        return None
    stack = json.loads(row["operation_stack"])
    if not stack:
        conn.close()
        return None
    undo_data = stack.pop()
    conn.execute(
        "UPDATE sessions SET operation_stack = ?, updated_at = ? WHERE id = ?",
        (json.dumps(stack, ensure_ascii=False), datetime.now(), session_id)
    )
    conn.commit()
    conn.close()
    logger.info(f"弹出撤回操作从会话 {session_id}: {undo_data.get('method', 'unknown')}")
    return undo_data

def clear_operations(session_id):
    conn = _get_conn()
    conn.execute(
        "UPDATE sessions SET operation_stack = '[]', updated_at = ? WHERE id = ?",
        (datetime.now(), session_id)
    )
    conn.commit()
    conn.close()

def get_operation_stack_size(session_id):
    conn = _get_conn()
    row = conn.execute(
        "SELECT operation_stack FROM sessions WHERE id = ?", (session_id,)
    ).fetchone()
    conn.close()
    if not row:
        return 0
    stack = json.loads(row["operation_stack"])
    return len(stack)

def get_session(session_id):
    conn = _get_conn()
    row = conn.execute(
        "SELECT id, title, created_at, updated_at FROM sessions WHERE id = ?",
        (session_id,)
    ).fetchone()
    conn.close()
    if not row:
        return None
    return {
        "id": row["id"],
        "title": row["title"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"]
    }
