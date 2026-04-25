import os
import json
import copy
from openai import OpenAI

from module_lg import get_logger

logger = get_logger("智能体")

KNOWLEDGE_DIR = os.path.join(os.path.dirname(__file__), "afgitbook", "english")

def _load_knowledge():
    parts = []
    base = KNOWLEDGE_DIR
    if not os.path.isdir(base):
        logger.warning(f"ADOFAI 文档目录不存在: {base}")
        return ""
    for root, dirs, files in os.walk(base):
        for fname in sorted(files):
            if not fname.endswith(".md"):
                continue
            fpath = os.path.join(root, fname)
            rel = os.path.relpath(fpath, base)
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                parts.append(f"===== {rel} =====\n{content}")
            except Exception as e:
                logger.warning(f"读取文档 {rel} 失败: {e}")
    if not parts:
        logger.warning("ADOFAI 文档目录为空")
        return ""
    logger.info(f"已加载 {len(parts)} 个 ADOFAI 文档文件")
    return "\n\n".join(parts)

KNOWLEDGE_TEXT = _load_knowledge()

SYSTEM_PROMPT = f"""你是一名 ADOFAI（冰与火之舞）谱面制作助手。你可以通过调用工具来操作 .adofai 关卡文件。

你的能力包括：
- 查看和修改关卡设置（settings）
- 添加、删除和编辑砖块（angleData或者pathData）
- 添加、删除和编辑事件（actions）
- 批量编辑事件
- 添加、删除和编辑装饰物（decorations）
- 统计事件和装饰物数量
- 导出 / 保存关卡文件

工作流程：
1. 首先理解用户的需求
2. 如果需要查看数据，先调用 get_level_info / get_tile_event / get_event_count 等查询工具
3. 根据查询结果决定修改操作
4. 每次工具调用后，我会告诉你执行结果
5. 最后用自然语言总结你做了什么，不要进一步说明是否需要更多操作，语言简洁

重要规则：
- 查看数据时，只查看需要用到的数据。例如用户询问关卡音高时，调用get_level_info方法时，fields参数只填入'pitch'
- 每次只进行必要的操作，不要做多余的修改
- 修改数据前先确认当前值
- 如果用户要求不明确，先问清楚再操作
- **如果遇到不理解的术语或概念，不要瞎猜，而是查阅下方提供的 ADOFAI 官方完整文档来获取准确信息**
- 如果用户提到的功能你不确定如何实现，告诉用户查阅相关官方文档
- 官方文档中有对每个事件的属性说明，在关卡文件中，这些属性以驼峰式命名法表示，例如：
    - MoveTrack在文档中有"Position offset"属性，而在关卡文件中则是"positionOffset"

以下是 ADOFAI 官方完整文档内容，供你随时查阅。如果你遇到不理解的术语、事件类型、参数含义等，直接在这份文档中搜索即可找到准确答案，不要猜测：
{KNOWLEDGE_TEXT}"""

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_level_summary",
            "description": "获取当前加载的关卡摘要信息，包括歌曲名、作者、BPM、offset、砖块数量、事件数量、装饰物数量",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_level_info",
            "description": "获取关卡 settings 下指定字段的值。不传 field 时返回 settings 下所有字段；传 'levelbase' 返回 song/artist/author；传多个字段合并返回；传单个字段直接返回值",
            "parameters": {
                "type": "object",
                "properties": {
                    "fields": {"type": "array", "items": {"type": "string"}, "description": "要获取的字段名列表，如 ['song','bpm','offset','artist','author']"}
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "edit_level_info",
            "description": "修改关卡 settings 中的字段值。可同时修改多个字段，如 song、bpm、offset、artist、author 等",
            "parameters": {
                "type": "object",
                "properties": {
                    "properties": {
                        "type": "object",
                        "description": "要修改的字段键值对，如 {\"song\": \"新歌名\", \"bpm\": 180, \"offset\": 100, \"artist\": \"艺术家\"}"
                    }
                },
                "required": ["properties"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "export_level",
            "description": "将当前关卡数据导出保存到文件。as_original=True 时使用 .adofai 格式（加 BOM），否则为标准 JSON 格式",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {"type": "string", "description": "保存路径，如 /path/to/level.adofai"},
                    "as_original": {"type": "boolean", "description": "是否以 .adofai 原始格式导出（加 BOM）", "default": False}
                },
                "required": ["filepath"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_tile_event",
            "description": "获取指定 floor 上的事件列表。可只传 floor 获取该 floor 所有事件，也可额外传 event_type 过滤特定类型",
            "parameters": {
                "type": "object",
                "properties": {
                    "floor": {"type": "integer", "description": "砖块编号（从 1 开始）"},
                    "event_type": {"type": "string", "description": "事件类型名称，如 MoveTrack、SetSpeed、Twirl 等（可选）"}
                },
                "required": ["floor"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_event_count",
            "description": "统计事件数量。可统计全局、按 floor、按 event_type 或组合统计",
            "parameters": {
                "type": "object",
                "properties": {
                    "floor": {"type": "integer", "description": "砖块编号（可选）"},
                    "event_type": {"type": "string", "description": "事件类型名称（可选）"}
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "batch_get_event_info",
            "description": "批量获取全关卡中所有指定类型事件的信息。可选择只返回特定属性",
            "parameters": {
                "type": "object",
                "properties": {
                    "event_type": {"type": "string", "description": "事件类型名称，如 MoveDecorations、SetSpeed 等"},
                    "attr": {"type": "string", "description": "只返回该属性（可选）"}
                },
                "required": ["event_type"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_event_info",
            "description": "获取指定 floor 上指定类型的第 index 个事件的详细信息。可指定返回特定属性",
            "parameters": {
                "type": "object",
                "properties": {
                    "floor": {"type": "integer", "description": "砖块编号（从 1 开始）"},
                    "event_type": {"type": "string", "description": "事件类型名称"},
                    "index": {"type": "integer", "description": "同类型事件的索引（从 0 开始，默认 0）", "default": 0},
                    "attrs": {"type": "array", "items": {"type": "string"}, "description": "要返回的属性名列表，如 ['duration','tag']（可选）"}
                },
                "required": ["floor", "event_type"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "edit_event_info",
            "description": "编辑指定 floor 上指定类型的第 index 个事件的属性",
            "parameters": {
                "type": "object",
                "properties": {
                    "floor": {"type": "integer", "description": "砖块编号（从 1 开始）"},
                    "event_type": {"type": "string", "description": "事件类型名称"},
                    "index": {"type": "integer", "description": "同类型事件的索引（从 0 开始，默认 0）", "default": 0},
                    "properties": {"type": "object", "description": "要修改的属性键值对，如 {\"duration\": 2, \"angleOffset\": 180}"}
                },
                "required": ["floor", "event_type", "properties"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "batch_edit_event",
            "description": "批量修改全关卡或指定 floor 上某类型事件的所有属性",
            "parameters": {
                "type": "object",
                "properties": {
                    "event_type": {"type": "string", "description": "事件类型名称"},
                    "floor": {"type": "integer", "description": "只修改该 floor 上的事件（可选，不填则全关卡）"},
                    "properties": {"type": "object", "description": "要修改的属性键值对"}
                },
                "required": ["event_type", "properties"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "add_event",
            "description": "向指定 floor 添加一个事件。可用 use_default 使用默认属性，或用 extra 传入自定义属性",
            "parameters": {
                "type": "object",
                "properties": {
                    "floor": {"type": "integer", "description": "砖块编号（从 1 开始）"},
                    "event_type": {"type": "string", "description": "事件类型名称，如 MoveTrack、SetSpeed、Twirl、SetHitsound 等"},
                    "use_default": {"type": "boolean", "description": "是否使用该事件类型的默认属性", "default": False},
                    "extra": {"type": "object", "description": "自定义属性键值对，如 {\"speedType\": \"Bpm\", \"beatsPerMinute\": 200}", "default": {}}
                },
                "required": ["floor", "event_type"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "remove_event",
            "description": "删除事件。可按 floor、event_type、index 组合删除。不传参数时清空所有事件",
            "parameters": {
                "type": "object",
                "properties": {
                    "floor": {"type": "integer", "description": "砖块编号（可选）。不填可全局按 event_type 删除"},
                    "event_type": {"type": "string", "description": "事件类型名称（可选）。不填则删除该 floor 上所有事件"},
                    "index": {"type": "integer", "description": "同类型事件的索引（可选）。不填删除全部匹配事件"}
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_tile_decoration",
            "description": "获取指定 floor 上的装饰物列表。可只传 floor，也可额外传 decoration_type 过滤",
            "parameters": {
                "type": "object",
                "properties": {
                    "floor": {"type": "integer", "description": "砖块编号（从 1 开始）"},
                    "decoration_type": {"type": "string", "description": "装饰物类型名称，如 AddDecoration、AddText 等（可选）"}
                },
                "required": ["floor"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_decoration_count",
            "description": "统计装饰物数量。可全局、按 floor、按 decoration_type 或组合统计",
            "parameters": {
                "type": "object",
                "properties": {
                    "floor": {"type": "integer", "description": "砖块编号（可选）"},
                    "decoration_type": {"type": "string", "description": "装饰物类型名称（可选）"}
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "batch_get_decoration_info",
            "description": "批量获取全关卡中所有指定类型装饰物的信息。可选择只返回特定属性",
            "parameters": {
                "type": "object",
                "properties": {
                    "decoration_type": {"type": "string", "description": "装饰物类型名称，如 AddDecoration 等"},
                    "attr": {"type": "string", "description": "只返回该属性（可选）"}
                },
                "required": ["decoration_type"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_decoration_info",
            "description": "获取指定 floor 上指定类型的第 index 个装饰物的详细信息。可指定返回特定属性",
            "parameters": {
                "type": "object",
                "properties": {
                    "floor": {"type": "integer", "description": "砖块编号（从 1 开始）"},
                    "decoration_type": {"type": "string", "description": "装饰物类型名称"},
                    "index": {"type": "integer", "description": "同类型装饰物的索引（从 0 开始，默认 0）", "default": 0},
                    "attrs": {"type": "array", "items": {"type": "string"}, "description": "要返回的属性名列表（可选）"}
                },
                "required": ["floor", "decoration_type"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "edit_decoration_info",
            "description": "编辑指定 floor 上指定类型的第 index 个装饰物的属性",
            "parameters": {
                "type": "object",
                "properties": {
                    "floor": {"type": "integer", "description": "砖块编号（从 1 开始）"},
                    "decoration_type": {"type": "string", "description": "装饰物类型名称"},
                    "index": {"type": "integer", "description": "同类型装饰物的索引（从 0 开始，默认 0）", "default": 0},
                    "properties": {"type": "object", "description": "要修改的属性键值对"}
                },
                "required": ["floor", "decoration_type", "properties"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "batch_edit_decoration",
            "description": "批量修改全关卡或指定 floor 上某类型装饰物的所有属性",
            "parameters": {
                "type": "object",
                "properties": {
                    "decoration_type": {"type": "string", "description": "装饰物类型名称"},
                    "floor": {"type": "integer", "description": "只修改该 floor 上的装饰物（可选，不填则全关卡）"},
                    "properties": {"type": "object", "description": "要修改的属性键值对"}
                },
                "required": ["decoration_type", "properties"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "add_decoration",
            "description": "向指定 floor 添加一个装饰物。可用 use_default 使用默认属性，或用 extra 传入自定义属性",
            "parameters": {
                "type": "object",
                "properties": {
                    "floor": {"type": "integer", "description": "砖块编号（从 1 开始）"},
                    "decoration_type": {"type": "string", "description": "装饰物类型名称，如 AddDecoration、AddText 等"},
                    "use_default": {"type": "boolean", "description": "是否使用该装饰物类型的默认属性", "default": False},
                    "extra": {"type": "object", "description": "装饰物的自定义属性键值对", "default": {}}
                },
                "required": ["floor", "decoration_type"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "remove_decoration",
            "description": "删除装饰物。可按 floor、decoration_type、index 组合删除。不传参数时清空所有装饰物",
            "parameters": {
                "type": "object",
                "properties": {
                    "floor": {"type": "integer", "description": "砖块编号（可选）"},
                    "decoration_type": {"type": "string", "description": "装饰物类型名称（可选）"},
                    "index": {"type": "integer", "description": "同类型装饰物的索引（可选，不填删除全部）"}
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "edit_angledata",
            "description": "在 angleData 的指定位置插入新的轨道角度数据。index 为插入位置（从 0 开始），part 为要插入的角度值列表",
            "parameters": {
                "type": "object",
                "properties": {
                    "index": {"type": "integer", "description": "插入位置索引（从 0 开始），新的轨道会插入到 angleData 的第 index 个位置"},
                    "part": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "要插入的轨道角度数据列表，如 [0, 180, 0]"
                    }
                },
                "required": ["index", "part"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_angledata",
            "description": "读取 angleData（轨道角度数据）的指定片段。angleData 是包含所有砖块角度信息的列表，索引从 0 开始计数：第 1 个砖块的索引为 0，第 2 个砖块的索引为 1，以此类推。不填参数返回所有砖块的 angleData",
            "parameters": {
                "type": "object",
                "properties": {
                    "start": {"type": "integer", "description": "起始砖块的索引值（从 0 开始，可选）。只填 start 时返回从该索引到最后一个砖块的数据"},
                    "end": {"type": "integer", "description": "终止砖块的索引值（不包含，可选）。只填 end 时返回第 0 个砖块到第 end-1 个砖块的数据"}
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "remove_angledata",
            "description": "删除 angleData（轨道角度数据）的指定片段。不填参数时删除所有砖块的 angleData；只填 start 时删除从该索引到末尾的砖块；只填 end 时删除从开头到 end-1 的砖块；填 start 和 end 时删除 [start, end) 范围的砖块",
            "parameters": {
                "type": "object",
                "properties": {
                    "start": {"type": "integer", "description": "起始砖块的索引值（从 0 开始，可选）。不填则从第 0 个砖块开始删除"},
                    "end": {"type": "integer", "description": "终止砖块的索引值（不包含，可选）。不填则删除到最后一个砖块"}
                },
                "required": []
            }
        }
    }
]


class AssistantAgent:
    def __init__(self):
        self.api_key = self._load_api_key_from_config()
        self._init_client()

    def _config_path(self):
        return os.path.join(os.path.dirname(__file__), "config.yaml")

    def _load_api_key_from_config(self) -> str:
        path = self._config_path()
        try:
            if os.path.isfile(path):
                with open(path, "r", encoding="utf-8") as f:
                    for line in f:
                        if line.startswith("deepseek_api_key:"):
                            key = line.split(":", 1)[1].strip().strip("'\"").strip("'")
                            if key:
                                return key
        except Exception:
            pass
        return os.environ.get("DEEPSEEK_API_KEY", "")

    def _save_api_key_to_config(self, api_key: str):
        path = self._config_path()
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(f'deepseek_api_key: "{api_key}"\n')
            logger.info(f"API Key 已保存到 {path}")
        except Exception as e:
            logger.error(f"保存 API Key 到配置文件失败: {e}")

    def _init_client(self):
        if self.api_key:
            self.client = OpenAI(
                api_key=self.api_key,
                base_url="https://api.deepseek.com"
            )
            logger.info("DeepSeek 客户端已创建")
        else:
            self.client = None
            logger.warning("未设置 DEEPSEEK_API_KEY 环境变量")

    def set_api_key(self, api_key: str):
        self.api_key = api_key
        self._init_client()
        self._save_api_key_to_config(api_key)
        return bool(self.api_key)

    def is_ready(self) -> bool:
        return self.client is not None

    MAX_HISTORY_TOKENS = 8000

    @staticmethod
    def _estimate_tokens(text: str) -> int:
        if not text:
            return 0
        return int(len(text) * 0.4) + 1

    def _db_messages_to_api(self, db_messages, max_tokens=MAX_HISTORY_TOKENS):
        """
        将数据库消息转换为 OpenAI API 消息格式，并控制 Token 预算。
        返回: list[dict] — API 格式的消息列表（按时间正序）
        """
        api_messages = []
        for msg in db_messages:
            role = msg.get("role")
            content = msg.get("content")

            if role == "system":
                continue

            if role == "user":
                api_messages.append({"role": "user", "content": content or ""})

            elif role == "assistant":
                tc = msg.get("tool_calls")
                if tc:
                    api_tc = {
                        "id": tc.get("tool_call_id", ""),
                        "type": "function",
                        "function": {
                            "name": tc.get("function_name", ""),
                            "arguments": json.dumps(tc.get("arguments", {}), ensure_ascii=False)
                        }
                    }
                    api_messages.append({
                        "role": "assistant",
                        "content": None,
                        "tool_calls": [api_tc]
                    })
                    api_messages.append({
                        "role": "tool",
                        "tool_call_id": tc.get("tool_call_id", ""),
                        "content": json.dumps(tc.get("result", {}), ensure_ascii=False)
                    })
                else:
                    api_messages.append({"role": "assistant", "content": content or ""})

        if not api_messages:
            return []

        total_tokens = sum(self._estimate_tokens(json.dumps(m, ensure_ascii=False)) for m in api_messages)

        while total_tokens > max_tokens and len(api_messages) > 4:
            removed = api_messages.pop(0)
            total_tokens -= self._estimate_tokens(json.dumps(removed, ensure_ascii=False))
            if len(api_messages) > 0:
                removed2 = api_messages.pop(0) if api_messages[0].get("role") == "tool" else None
                if removed2:
                    total_tokens -= self._estimate_tokens(json.dumps(removed2, ensure_ascii=False))

        return api_messages

    def _execute_tool(self, tool_name, tool_args, level):
        undo = None
        result = None

        try:
            if tool_name == "get_level_summary":
                settings = level.data.get("settings", {})
                result = {
                    "song": settings.get("song", "未知"),
                    "artist": settings.get("artist", "未知"),
                    "author": settings.get("author", "未知"),
                    "bpm": settings.get("bpm", "未知"),
                    "offset": settings.get("offset", 0),
                    "tile_count": len(level.data.get("angleData", [])),
                    "event_count": len(level.data.get("actions", [])),
                    "decoration_count": len(level.data.get("decorations", []))
                }

            elif tool_name == "get_level_info":
                fields = tool_args.get("fields", [])
                if not fields:
                    result = level.get_level_info()
                elif len(fields) == 1:
                    val = level.get_level_info(fields[0])
                    result = {fields[0]: val}
                else:
                    result = level.get_level_info(*fields)

            elif tool_name == "edit_level_info":
                from adobase.params import LEVEL_PARAMS as LevelParamsSet
                properties = tool_args["properties"]
                old_values = {}
                settings = level.data.get("settings", {})
                for k in properties:
                    if k in LevelParamsSet:
                        old_values[k] = settings.get(k)
                level.edit_level_info(**properties)
                undo = {"method": "edit_level_info", "params": {"old": old_values}, "original_tool": tool_name, "original_args": tool_args}
                result = {"modified": list(properties.keys()), "new_values": properties}

            elif tool_name == "export_level":
                filepath = tool_args["filepath"]
                as_original = tool_args.get("as_original", False)
                level.export(filepath, as_original=as_original)
                result = {"exported": True, "filepath": filepath, "as_original": as_original}

            elif tool_name == "get_tile_event":
                floor = tool_args["floor"]
                event_type = tool_args.get("event_type")
                events = level.get_tile_event(floor, event_type)
                result = {"floor": floor, "count": len(events), "events": events[:30], "truncated": len(events) > 30}

            elif tool_name == "get_event_count":
                floor = tool_args.get("floor")
                event_type = tool_args.get("event_type")
                count = level.get_event_count(floor=floor, event_type=event_type)
                result = {"count": count, "floor": floor, "event_type": event_type}

            elif tool_name == "batch_get_event_info":
                event_type = tool_args["event_type"]
                attr = tool_args.get("attr")
                data = level.batch_get_event_info(event_type, attr=attr)
                result = {"event_type": event_type, "count": len(data), "data": data[:30], "truncated": len(data) > 30}

            elif tool_name == "get_event_info":
                floor = tool_args["floor"]
                event_type = tool_args["event_type"]
                index = tool_args.get("index", 0)
                attrs = tool_args.get("attrs", [])
                if attrs:
                    info = level.get_event_info(floor, event_type, index, *attrs)
                else:
                    info = level.get_event_info(floor, event_type, index)
                result = {"floor": floor, "event_type": event_type, "index": index, "info": info}

            elif tool_name == "edit_event_info":
                floor = tool_args["floor"]
                event_type = tool_args["event_type"]
                index = tool_args.get("index", 0)
                properties = tool_args["properties"]
                events = level.get_tile_event(floor, event_type)
                if not events or index < 0 or index >= len(events):
                    raise IndexError(f"floor={floor} event_type={event_type} index={index} 不存在")
                old_values = {}
                for k in properties:
                    old_values[k] = events[index].get(k)
                level.edit_event_info(floor, event_type, index, **properties)
                undo = {"method": "edit_event_info", "params": {"floor": floor, "event_type": event_type, "index": index, "old": old_values}, "original_tool": tool_name, "original_args": tool_args}
                result = {"modified": True, "floor": floor, "event_type": event_type, "new_values": properties}

            elif tool_name == "batch_edit_event":
                event_type = tool_args["event_type"]
                floor = tool_args.get("floor")
                properties = tool_args["properties"]
                all_events = level.batch_get_event_info(event_type)
                old_values_list = []
                for ev in all_events:
                    ev_old = {}
                    for k in properties:
                        ev_old[k] = ev.get(k)
                    old_values_list.append(ev_old)
                count = level.batch_edit_event(event_type, floor=floor, **properties)
                undo = {"method": "batch_edit_event_undo", "params": {"event_type": event_type, "floor": floor, "old_list": old_values_list}, "original_tool": tool_name, "original_args": tool_args}
                result = {"modified_count": count, "event_type": event_type, "new_values": properties}

            elif tool_name == "add_event":
                floor = tool_args["floor"]
                event_type = tool_args["event_type"]
                use_default = tool_args.get("use_default", False)
                extra = tool_args.get("extra", {})
                if use_default:
                    level.add_event(floor, event_type, "default")
                else:
                    level.add_event(floor, event_type, **extra)
                undo = {"method": "remove_event", "params": {"floor": floor, "event_type": event_type}, "original_tool": tool_name, "original_args": tool_args}
                result = {"added": True, "floor": floor, "event_type": event_type}

            elif tool_name == "remove_event":
                floor = tool_args.get("floor")
                event_type = tool_args.get("event_type")
                index = tool_args.get("index")
                removed = level.remove_event(floor=floor, event_type=event_type, index=index)
                if isinstance(removed, list):
                    undo = {"method": "add_events_batch", "params": {"events": [copy.deepcopy(e) for e in removed]}, "original_tool": tool_name, "original_args": tool_args}
                    result = {"removed_count": len(removed)}
                else:
                    undo = {"method": "add_event_restore", "params": {"event": copy.deepcopy(removed)}, "original_tool": tool_name, "original_args": tool_args}
                    result = {"removed": True, "event": removed}

            elif tool_name == "get_tile_decoration":
                floor = tool_args["floor"]
                decoration_type = tool_args.get("decoration_type")
                decos = level.get_tile_decoration(floor, decoration_type)
                result = {"floor": floor, "count": len(decos), "decorations": decos[:30], "truncated": len(decos) > 30}

            elif tool_name == "get_decoration_count":
                floor = tool_args.get("floor")
                decoration_type = tool_args.get("decoration_type")
                count = level.get_decoration_count(floor=floor, decoration_type=decoration_type)
                result = {"count": count, "floor": floor, "decoration_type": decoration_type}

            elif tool_name == "batch_get_decoration_info":
                decoration_type = tool_args["decoration_type"]
                attr = tool_args.get("attr")
                data = level.batch_get_decoration_info(decoration_type, attr=attr)
                result = {"decoration_type": decoration_type, "count": len(data), "data": data[:30], "truncated": len(data) > 30}

            elif tool_name == "get_decoration_info":
                floor = tool_args["floor"]
                decoration_type = tool_args["decoration_type"]
                index = tool_args.get("index", 0)
                attrs = tool_args.get("attrs", [])
                if attrs:
                    info = level.get_decoration_info(floor, decoration_type, index, *attrs)
                else:
                    info = level.get_decoration_info(floor, decoration_type, index)
                result = {"floor": floor, "decoration_type": decoration_type, "index": index, "info": info}

            elif tool_name == "edit_decoration_info":
                floor = tool_args["floor"]
                decoration_type = tool_args["decoration_type"]
                index = tool_args.get("index", 0)
                properties = tool_args["properties"]
                decos = level.get_tile_decoration(floor, decoration_type)
                if not decos or index < 0 or index >= len(decos):
                    raise IndexError(f"floor={floor} decoration_type={decoration_type} index={index} 不存在")
                old_values = {}
                for k in properties:
                    old_values[k] = decos[index].get(k)
                level.edit_decoration_info(floor, decoration_type, index, **properties)
                undo = {"method": "edit_decoration_info", "params": {"floor": floor, "decoration_type": decoration_type, "index": index, "old": old_values}, "original_tool": tool_name, "original_args": tool_args}
                result = {"modified": True, "floor": floor, "decoration_type": decoration_type, "new_values": properties}

            elif tool_name == "batch_edit_decoration":
                decoration_type = tool_args["decoration_type"]
                floor = tool_args.get("floor")
                properties = tool_args["properties"]
                all_decos = level.batch_get_decoration_info(decoration_type)
                old_values_list = []
                for d in all_decos:
                    d_old = {}
                    for k in properties:
                        d_old[k] = d.get(k)
                    old_values_list.append(d_old)
                count = level.batch_edit_decoration(decoration_type, floor=floor, **properties)
                undo = {"method": "batch_edit_decoration_undo", "params": {"decoration_type": decoration_type, "floor": floor, "old_list": old_values_list}, "original_tool": tool_name, "original_args": tool_args}
                result = {"modified_count": count, "decoration_type": decoration_type, "new_values": properties}

            elif tool_name == "add_decoration":
                floor = tool_args["floor"]
                decoration_type = tool_args["decoration_type"]
                use_default = tool_args.get("use_default", False)
                extra = tool_args.get("extra", {})
                if use_default:
                    level.add_decoration(floor, decoration_type, "default")
                else:
                    level.add_decoration(floor, decoration_type, **extra)
                undo = {"method": "remove_decoration", "params": {"floor": floor, "decoration_type": decoration_type}, "original_tool": tool_name, "original_args": tool_args}
                result = {"added": True, "floor": floor, "decoration_type": decoration_type}

            elif tool_name == "remove_decoration":
                floor = tool_args.get("floor")
                decoration_type = tool_args.get("decoration_type")
                index = tool_args.get("index")
                removed = level.remove_decoration(floor=floor, decoration_type=decoration_type, index=index)
                if isinstance(removed, list):
                    undo = {"method": "add_decorations_batch", "params": {"decorations": [copy.deepcopy(d) for d in removed]}, "original_tool": tool_name, "original_args": tool_args}
                    result = {"removed_count": len(removed)}
                else:
                    undo = {"method": "add_decoration_restore", "params": {"decoration": copy.deepcopy(removed)}, "original_tool": tool_name, "original_args": tool_args}
                    result = {"removed": True, "decoration": removed}

            elif tool_name == "edit_angledata":
                index = tool_args["index"]
                part = tool_args["part"]
                level.edit_angledata(index, part)
                undo = {"method": "edit_angledata_undo", "params": {"index": index}, "original_tool": tool_name, "original_args": tool_args}
                result = {"modified": True, "index": index, "part": part}

            elif tool_name == "get_angledata":
                start = tool_args.get("start")
                end = tool_args.get("end")
                data = level.get_angledata(start=start, end=end)
                total = len(level.data.get("angleData", []))
                result = {"count": len(data), "total": total, "start": start, "end": end, "data": data[:50], "truncated": len(data) > 50}

            elif tool_name == "remove_angledata":
                start = tool_args.get("start")
                end = tool_args.get("end")
                removed = level.remove_angledata(start=start, end=end)
                undo = {"method": "remove_angledata_undo", "params": {"removed": copy.deepcopy(removed), "start": start, "end": end}, "original_tool": tool_name, "original_args": tool_args}
                result = {"removed_count": len(removed), "start": start, "end": end}

            else:
                result = {"error": f"未知工具: {tool_name}"}

        except Exception as e:
            result = {"error": str(e)}
            undo = None
            logger.error(f"工具执行失败 {tool_name}: {e}")

        return result, undo

    def _execute_undo(self, undo_data, level):
        method = undo_data.get("method")
        params = undo_data.get("params", {})

        def _restore_edit_level_info():
            settings = level.data.setdefault("settings", {})
            for k, v in params.get("old", {}).items():
                settings[k] = v

        def _restore_edit_event(event, floor_key, event_type_key, index_key, old_key):
            events = level.get_tile_event(params[floor_key], params[event_type_key])
            idx = params.get(index_key, 0)
            if 0 <= idx < len(events):
                for k, v in params.get(old_key, {}).items():
                    events[idx][k] = v

        def _restore_batch_edit(event_type_key, old_list_key):
            old_list = params.get(old_list_key, [])
            for ev, old in zip(level.batch_get_event_info(params[event_type_key]), old_list):
                for k, v in old.items():
                    ev[k] = v

        try:
            if method == "edit_level_info":
                _restore_edit_level_info()
            elif method == "edit_event_info":
                _restore_edit_event(level, "floor", "event_type", "index", "old")
            elif method == "batch_edit_event_undo":
                _restore_batch_edit("event_type", "old_list")
            elif method == "edit_decoration_info":
                decos = level.get_tile_decoration(params["floor"], params["decoration_type"])
                idx = params.get("index", 0)
                if 0 <= idx < len(decos):
                    for k, v in params.get("old", {}).items():
                        decos[idx][k] = v
            elif method == "batch_edit_decoration_undo":
                old_list = params.get("old_list", [])
                for d, old in zip(level.batch_get_decoration_info(params["decoration_type"]), old_list):
                    for k, v in old.items():
                        d[k] = v
            elif method == "remove_event":
                level.remove_event(floor=params.get("floor"), event_type=params.get("event_type"), index=params.get("index"))
            elif method == "add_events_batch":
                actions = level.data.setdefault("actions", [])
                for event in params.get("events", []):
                    actions.append(event)
            elif method == "add_event_restore":
                event = params.get("event", {})
                actions = level.data.setdefault("actions", [])
                floor = event.get("floor", 0)
                insert_idx = None
                last_same_floor_idx = None
                for idx, act in enumerate(actions):
                    if act.get("floor") == floor:
                        last_same_floor_idx = idx
                if last_same_floor_idx is not None:
                    insert_idx = last_same_floor_idx + 1
                else:
                    for idx, act in enumerate(actions):
                        if act.get("floor", -1) > floor:
                            insert_idx = idx
                            break
                actions.insert(insert_idx, event) if insert_idx is not None else actions.append(event)
            elif method == "remove_decoration":
                level.remove_decoration(floor=params.get("floor"), decoration_type=params.get("decoration_type"), index=params.get("index"))
            elif method == "add_decorations_batch":
                decos = level.data.setdefault("decorations", [])
                for d in params.get("decorations", []):
                    decos.append(d)
            elif method == "add_decoration_restore":
                decoration = params.get("decoration", {})
                decos = level.data.setdefault("decorations", [])
                floor = decoration.get("floor", 0)
                insert_idx = None
                last_same_floor_idx = None
                for idx, item in enumerate(decos):
                    if item.get("floor") == floor:
                        last_same_floor_idx = idx
                if last_same_floor_idx is not None:
                    insert_idx = last_same_floor_idx + 1
                else:
                    for idx, item in enumerate(decos):
                        if item.get("floor", -1) > floor:
                            insert_idx = idx
                            break
                decos.insert(insert_idx, decoration) if insert_idx is not None else decos.append(decoration)
            elif method == "remove_angledata_undo":
                angle_data = level.data.setdefault("angleData", [])
                removed = params.get("removed", [])
                insert_pos = params.get("start", 0)
                if insert_pos is None:
                    insert_pos = 0
                for i, item in enumerate(removed):
                    angle_data.insert(insert_pos + i, item)
            elif method == "edit_angledata_undo":
                angle_data = level.data.get("angleData", [])
                idx = params.get("index", 0)
                if 0 <= idx < len(angle_data):
                    angle_data.pop(idx)
            else:
                logger.warning(f"未知的撤回方法: {method}")
                return False
            return True
        except Exception as e:
            logger.error(f"撤回操作失败 {method}: {e}")
            return False

    def chat(self, user_message, level, session_id):
        import database
        from adobase import ADOFAILevel

        if not self.is_ready():
            return "请先在设置中配置 DeepSeek API Key 后再开始对话。", False

        settings = level.data.get("settings", {})
        angle_data = level.data.get("angleData", [])
        level_context = (
            f"当前关卡信息：\n"
            f"- 歌曲: {settings.get('song', '未知')}\n"
            f"- 艺术家: {settings.get('artist', '未知')}\n"
            f"- 作者: {settings.get('author', '未知')}\n"
            f"- BPM: {settings.get('bpm', '未知')}\n"
            f"- Offset: {settings.get('offset', 0)}\n"
            f"- 总砖块数: {len(angle_data)}\n"
            f"- 总事件数: {len(level.data.get('actions', []))}\n"
            f"- 总装饰物数: {len(level.data.get('decorations', []))}"
        )

        db_history = database.get_recent_messages(session_id, 100)
        history_msgs = self._db_messages_to_api(db_history, self.MAX_HISTORY_TOKENS)

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "system", "content": level_context},
        ]
        messages.extend(history_msgs)
        messages.append({"role": "user", "content": user_message})

        all_messages_for_db = []
        all_messages_for_db.append({"role": "user", "content": user_message})

        max_iterations = 10
        final_reply = ""
        modified = False

        for iteration in range(max_iterations):
            try:
                response = self.client.chat.completions.create(
                    model="deepseek-chat",
                    messages=messages,
                    tools=TOOLS,
                    tool_choice="auto",
                    temperature=0.7,
                    max_tokens=4096
                )
            except Exception as e:
                logger.error(f"DeepSeek API 调用失败: {e}")
                error_msg = f"API 调用失败: {str(e)}"
                database.add_message(session_id, "assistant", error_msg)
                return error_msg, False

            choice = response.choices[0]
            msg = choice.message

            if msg.tool_calls:
                for tool_call in msg.tool_calls:
                    tool_name = tool_call.function.name
                    try:
                        tool_args = json.loads(tool_call.function.arguments)
                    except json.JSONDecodeError:
                        tool_args = {}

                    logger.info(f"执行工具: {tool_name} 参数: {tool_args}")

                    tool_result, undo_data = self._execute_tool(tool_name, tool_args, level)

                    if undo_data:
                        database.push_operation(session_id, undo_data)
                        modified = True

                    tool_result_str = json.dumps(tool_result, ensure_ascii=False)

                    storable = {
                        "tool_call_id": tool_call.id,
                        "function_name": tool_name,
                        "arguments": tool_args,
                        "result": tool_result
                    }
                    all_messages_for_db.append({"role": "assistant", "content": None, "tool_calls": storable})

                    messages.append({
                        "role": "assistant",
                        "content": None,
                        "tool_calls": [
                            {
                                "id": tool_call.id,
                                "type": "function",
                                "function": {
                                    "name": tool_name,
                                    "arguments": tool_call.function.arguments
                                }
                            }
                        ]
                    })
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": tool_result_str
                    })
            else:
                final_reply = msg.content or ""
                break
        else:
            final_reply = "操作已完成，但可能需要进一步确认。"

        if not final_reply:
            try:
                follow_up = self.client.chat.completions.create(
                    model="deepseek-chat",
                    messages=messages + [{"role": "user", "content": "请用中文总结你刚才执行的所有操作。"}],
                    temperature=0.7,
                    max_tokens=2048
                )
                final_reply = follow_up.choices[0].message.content or "操作已完成。"
            except Exception as e:
                final_reply = "操作已完成。"
                logger.error(f"获取总结失败: {e}")

        all_messages_for_db.append({"role": "assistant", "content": final_reply})

        for db_msg in all_messages_for_db:
            role = db_msg["role"]
            content = db_msg.get("content")
            tool_calls_data = db_msg.get("tool_calls")
            database.add_message(session_id, role, content, tool_calls_data)

        return final_reply, modified

