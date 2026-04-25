import os
import json
import uuid
import tempfile

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

import database
from agent import AssistantAgent
from adobase import ADOFAILevel
from module_parser import get_level_json
from module_lg import get_logger

logger = get_logger("后端API")

app = Flask(__name__)
CORS(app)

database.init_db()

agent = AssistantAgent()

loaded_levels = {}

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

loaded_level_paths = {}

# ==================== 前端页面 ====================

@app.route("/")
def index():
    return render_template("index.html")

# ==================== 会话管理 ====================

@app.route("/api/sessions", methods=["GET"])
def list_sessions():
    try:
        sessions = database.get_sessions()
        return jsonify({"sessions": sessions})
    except Exception as e:
        logger.error(f"获取会话列表失败: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/sessions", methods=["POST"])
def new_session():
    try:
        data = request.get_json() or {}
        title = data.get("title", "新会话")
        session = database.create_session(title)
        return jsonify(session)
    except Exception as e:
        logger.error(f"创建会话失败: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/sessions/<session_id>", methods=["PUT"])
def rename_session(session_id):
    try:
        session = database.get_session(session_id)
        if not session:
            return jsonify({"error": "会话不存在"}), 404
        data = request.get_json() or {}
        title = data.get("title", session["title"])
        result = database.update_session_title(session_id, title)
        return jsonify(result)
    except Exception as e:
        logger.error(f"重命名会话失败: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/sessions/<session_id>", methods=["DELETE"])
def remove_session(session_id):
    try:
        session = database.get_session(session_id)
        if not session:
            return jsonify({"error": "会话不存在"}), 404
        database.delete_session(session_id)
        if session_id in loaded_levels:
            del loaded_levels[session_id]
        if session_id in loaded_level_paths:
            del loaded_level_paths[session_id]
        return jsonify({"deleted": session_id})
    except Exception as e:
        logger.error(f"删除会话失败: {e}")
        return jsonify({"error": str(e)}), 500

app.config['SECRET_KEY'] = os.urandom(24)

# ==================== API Key 管理 ====================

@app.route("/api/api_key_status", methods=["GET"])
def api_key_status():
    configured = agent.is_ready()
    has_env = bool(os.environ.get("DEEPSEEK_API_KEY", ""))
    return jsonify({
        "configured": configured,
        "has_env_var": has_env,
        "hint": "API Key 未配置，请在设置中填入密钥" if not configured else None
    })

@app.route("/api/set_api_key", methods=["POST"])
def set_api_key():
    try:
        data = request.get_json() or {}
        api_key = data.get("api_key", "").strip()
        if not api_key:
            return jsonify({"error": "API Key 不能为空"}), 400
        agent.set_api_key(api_key)
        os.environ["DEEPSEEK_API_KEY"] = api_key
        logger.info("API Key 已通过前端设置")
        return jsonify({"configured": True})
    except Exception as e:
        logger.error(f"设置 API Key 失败: {e}")
        return jsonify({"error": str(e)}), 500

# ==================== 会话消息 ====================

@app.route("/api/sessions/<session_id>/messages", methods=["GET"])
def get_session_messages(session_id):
    try:
        session = database.get_session(session_id)
        if not session:
            return jsonify({"error": "会话不存在"}), 404
        messages = database.get_messages(session_id)
        undo_count = database.get_operation_stack_size(session_id)
        level_path = loaded_level_paths.get(session_id)
        level_info = None
        if session_id in loaded_levels:
            lvl = loaded_levels[session_id]
            settings = lvl.data.get("settings", {})
            level_info = {
                "song": settings.get("song", ""),
                "artist": settings.get("artist", ""),
                "bpm": settings.get("bpm"),
                "tile_count": len(lvl.data.get("angleData", []))
            }
        return jsonify({
            "messages": messages,
            "undo_count": undo_count,
            "level_path": level_path,
            "level_info": level_info
        })
    except Exception as e:
        logger.error(f"获取消息失败: {e}")
        return jsonify({"error": str(e)}), 500

# ==================== 关卡加载 ====================

@app.route("/api/load_level", methods=["POST"])
def load_level():
    try:
        session_id = request.form.get("session_id")
        file_path = request.form.get("file_path")

        if not session_id:
            return jsonify({"error": "缺少 session_id"}), 400

        session = database.get_session(session_id)
        if not session:
            return jsonify({"error": "会话不存在"}), 404

        if file_path:
            if not os.path.isfile(file_path):
                return jsonify({"error": f"文件不存在: {file_path}"}), 400
            actual_path = file_path
        elif "file" in request.files:
            file = request.files["file"]
            if file.filename == "":
                return jsonify({"error": "未选择文件"}), 400
            if not file.filename.endswith(".adofai"):
                return jsonify({"error": "仅支持 .adofai 文件"}), 400
            safe_name = f"{uuid.uuid4().hex}_{file.filename}"
            actual_path = os.path.join(UPLOAD_DIR, safe_name)
            file.save(actual_path)
            logger.info(f"上传文件保存到: {actual_path}")
        else:
            return jsonify({"error": "请提供文件路径或上传文件"}), 400

        raw_data = get_level_json(actual_path)
        level = ADOFAILevel(raw_data)
        loaded_levels[session_id] = level
        loaded_level_paths[session_id] = actual_path

        settings = level.data.get("settings", {})
        info = {
            "file_path": actual_path,
            "song": settings.get("song", ""),
            "artist": settings.get("artist", ""),
            "author": settings.get("author", ""),
            "bpm": settings.get("bpm"),
            "offset": settings.get("offset", 0),
            "tile_count": len(level.data.get("angleData", [])),
            "event_count": len(level.data.get("actions", [])),
            "decoration_count": len(level.data.get("decorations", []))
        }
        logger.info(f"加载关卡: {info['song']} (session={session_id})")
        return jsonify({"loaded": True, "level_info": info})
    except Exception as e:
        logger.error(f"加载关卡失败: {e}")
        return jsonify({"error": str(e)}), 500

# ==================== 聊天 ====================

@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json() or {}
        session_id = data.get("session_id")
        message = data.get("message", "").strip()

        if not session_id:
            return jsonify({"error": "缺少 session_id"}), 400
        if not message:
            return jsonify({"error": "消息不能为空"}), 400

        session = database.get_session(session_id)
        if not session:
            return jsonify({"error": "会话不存在"}), 404

        if session_id not in loaded_levels:
            return jsonify({"error": "请先加载一个 .adofai 关卡文件"}), 400

        level = loaded_levels[session_id]
        level_path = loaded_level_paths.get(session_id)

        logger.info(f"会话 {session_id}: 用户消息 - {message[:80]}...")

        reply, modified = agent.chat(message, level, session_id)

        if modified and level_path:
            from datetime import datetime
            import re
            now = datetime.now()
            time_str = now.strftime("%H_%M_%d%m%y")
            dir_name = os.path.dirname(level_path)
            base_name = os.path.splitext(os.path.basename(level_path))[0]
            base_name = re.sub(r'^[0-9a-f]{32}_', '', base_name)
            backup_path = os.path.join(dir_name, f"{base_name}_{time_str}.adofai")
            level.export(backup_path, as_original=True)
            logger.info(f"关卡已保存到: {backup_path}")

        settings = level.data.get("settings", {})
        undo_count = database.get_operation_stack_size(session_id)

        return jsonify({
            "reply": reply,
            "level_info": {
                "song": settings.get("song", ""),
                "artist": settings.get("artist", ""),
                "bpm": settings.get("bpm"),
                "tile_count": len(level.data.get("angleData", []))
            },
            "undo_count": undo_count
        })
    except Exception as e:
        logger.error(f"聊天处理失败: {e}")
        return jsonify({"error": str(e)}), 500

# ==================== 撤回 ====================

@app.route("/api/undo/<session_id>", methods=["POST"])
def undo_operation(session_id):
    try:
        session = database.get_session(session_id)
        if not session:
            return jsonify({"error": "会话不存在"}), 404

        if session_id not in loaded_levels:
            return jsonify({"error": "请先加载关卡文件"}), 400

        undo_data = database.pop_operation(session_id)
        if not undo_data:
            return jsonify({"undone": False, "message": "没有可撤回的操作"})

        level = loaded_levels[session_id]
        level_path = loaded_level_paths.get(session_id)

        success = agent._execute_undo(undo_data, level)

        if success and level_path:
            level.export(level_path, as_original=True)

            original_tool = undo_data.get("original_tool", "unknown")
            original_args = undo_data.get("original_args", {})
            summary = (
                f"↩ **操作已撤回**\n\n"
                f"- **调用的工具**: `{original_tool}`\n"
                f"- **参数**: ```json\n{json.dumps(original_args, ensure_ascii=False, indent=2)}\n```"
            )
            database.add_message(session_id, "system", summary)

        undo_count = database.get_operation_stack_size(session_id)

        return jsonify({
            "undone": success,
            "method": undo_data.get("method", "unknown"),
            "remaining_undo": undo_count
        })
    except Exception as e:
        logger.error(f"撤回操作失败: {e}")
        return jsonify({"error": str(e)}), 500

# ==================== 启动 ====================

if __name__ == "__main__":
    logger.info("Assfai 服务启动")
    app.run(host="0.0.0.0", port=5000, debug=True)
