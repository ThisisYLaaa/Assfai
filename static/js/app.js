const API_BASE = window.location.origin;

let currentSessionId = null;
let currentLevelPath = null;
let currentUndoCount = 0;
let isLoading = false;

// ==================== 初始化 ====================
document.addEventListener("DOMContentLoaded", () => {
    checkApiKeyStatus();
    refreshSessionList();
    bindEvents();
});

function bindEvents() {
    document.getElementById("btn-new-session").addEventListener("click", createSession);
    document.getElementById("chat-form").addEventListener("submit", sendMessage);
    document.getElementById("btn-load-level").addEventListener("click", showLoadLevelModal);
    document.getElementById("btn-undo").addEventListener("click", undoLastOperation);
    document.getElementById("btn-settings").addEventListener("click", showSettingsModal);
    document.getElementById("btn-save-api-key").addEventListener("click", saveApiKey);
}

// ==================== 会话管理 ====================
async function refreshSessionList() {
    try {
        const res = await fetch(`${API_BASE}/api/sessions`);
        const data = await res.json();
        renderSessionList(data.sessions || []);
    } catch (e) {
        console.error("获取会话列表失败:", e);
    }
}

function renderSessionList(sessions) {
    const list = document.getElementById("session-list");
    if (sessions.length === 0) {
        list.innerHTML = `<div class="empty-state">
            <div class="icon">💬</div>
            <div class="text">暂无会话</div>
            <div class="hint">点击 + 新建会话</div>
        </div>`;
        return;
    }
    list.innerHTML = sessions.map(s => `
        <div class="session-item ${s.id === currentSessionId ? 'active' : ''}"
             onclick="switchSession('${s.id}')">
            <span class="session-title" title="${escapeHtml(s.title)}">${escapeHtml(s.title)}</span>
            <span class="session-meta">${s.message_count || 0}</span>
            <span class="session-actions" onclick="event.stopPropagation()">
                <button class="btn-icon" title="重命名" onclick="renameSessionPrompt('${s.id}', '${escapeHtml(s.title)}')">✏</button>
                <button class="btn-icon danger" title="删除" onclick="deleteSessionConfirm('${s.id}')">✕</button>
            </span>
        </div>
    `).join("");
}

async function createSession() {
    try {
        const res = await fetch(`${API_BASE}/api/sessions`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ title: "新会话" })
        });
        const session = await res.json();
        await refreshSessionList();
        switchSession(session.id);
    } catch (e) {
        console.error("创建会话失败:", e);
    }
}

async function switchSession(sessionId) {
    currentSessionId = sessionId;
    currentLevelPath = null;
    currentUndoCount = 0;
    await loadMessages();
    refreshSessionList();
}

async function renameSessionPrompt(sessionId, oldTitle) {
    const newTitle = prompt("输入新标题:", oldTitle);
    if (newTitle && newTitle.trim() && newTitle.trim() !== oldTitle) {
        try {
            await fetch(`${API_BASE}/api/sessions/${sessionId}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ title: newTitle.trim() })
            });
            refreshSessionList();
        } catch (e) {
            console.error("重命名失败:", e);
        }
    }
}

async function deleteSessionConfirm(sessionId) {
    if (!confirm("确定删除此会话？所有聊天记录将被清除。")) return;
    try {
        await fetch(`${API_BASE}/api/sessions/${sessionId}`, { method: "DELETE" });
        if (currentSessionId === sessionId) {
            currentSessionId = null;
            currentLevelPath = null;
            currentUndoCount = 0;
            renderMessages([]);
            updateToolbar(null);
        }
        refreshSessionList();
    } catch (e) {
        console.error("删除会话失败:", e);
    }
}

// ==================== 消息加载 ====================
async function loadMessages() {
    if (!currentSessionId) {
        renderMessages([]);
        updateToolbar(null);
        return;
    }
    try {
        const res = await fetch(`${API_BASE}/api/sessions/${currentSessionId}/messages`);
        const data = await res.json();
        currentLevelPath = data.level_path;
        currentUndoCount = data.undo_count || 0;
        updateToolbar(data.level_info);
        updateUndoButton();
        renderMessages(data.messages || []);
    } catch (e) {
        console.error("加载消息失败:", e);
    }
}

function renderMessages(messages) {
    const container = document.getElementById("chat-messages");
    if (!currentSessionId) {
        container.innerHTML = `<div class="empty-state">
            <div class="icon">🎵</div>
            <div class="text">选择一个会话或创建新会话</div>
            <div class="hint">加载 .adofai 文件后即可与 AI 对话</div>
        </div>`;
        document.getElementById("chat-input-area").style.display = "none";
        document.getElementById("chat-header").style.display = "none";
        return;
    }

    document.getElementById("chat-input-area").style.display = "block";
    document.getElementById("chat-header").style.display = "flex";

    if (messages.length === 0) {
        container.innerHTML = `<div class="empty-state">
            <div class="icon">🎵</div>
            <div class="text">开始对话</div>
            <div class="hint">向 AI 助手发送消息来操作关卡文件</div>
        </div>`;
        return;
    }

    container.innerHTML = messages.map(m => renderMessage(m)).join("");
    container.scrollTop = container.scrollHeight;
}

function renderMessage(m) {
    if (m.role === "user") {
        return `
            <div class="message user">
                <div class="avatar">👤</div>
                <div class="bubble">${renderMarkdown(m.content)}</div>
            </div>`;
    }

    if (m.role === "assistant") {
        if (m.tool_calls) {
            const tc = m.tool_calls;
            let resultPreview = "";
            if (tc.result) {
                resultPreview = JSON.stringify(tc.result, null, 2).substring(0, 300);
            }
            return `
                <div class="message assistant">
                    <div class="avatar">🤖</div>
                    <div class="bubble">
                        <div class="tool-call-info">
                            🔧 调用工具: <span class="tool-name">${escapeHtml(tc.function_name)}</span>
                            <br>参数: ${escapeHtml(JSON.stringify(tc.arguments))}
                            ${resultPreview ? `<div class="tool-result">${escapeHtml(resultPreview)}</div>` : ""}
                        </div>
                    </div>
                </div>`;
        }

        if (m.content) {
            return `
                <div class="message assistant">
                    <div class="avatar">🤖</div>
                    <div class="bubble">${renderMarkdown(m.content)}</div>
                </div>`;
        }

        return "";
    }

    return "";
}

function appendLoadingIndicator() {
    const container = document.getElementById("chat-messages");
    const loading = document.createElement("div");
    loading.className = "message assistant";
    loading.id = "loading-indicator";
    loading.innerHTML = `
        <div class="avatar">🤖</div>
        <div class="bubble">
            <div class="loading">
                <div class="spinner"></div>
                正在思考...
            </div>
        </div>`;
    container.appendChild(loading);
    container.scrollTop = container.scrollHeight;
}

function removeLoadingIndicator() {
    const el = document.getElementById("loading-indicator");
    if (el) el.remove();
}

// ==================== 聊天 ====================
async function sendMessage(e) {
    e.preventDefault();
    if (isLoading) return;

    const input = document.getElementById("chat-input");
    const message = input.value.trim();
    if (!message) return;

    if (!currentSessionId) {
        alert("请先创建或选择一个会话");
        return;
    }

    if (!currentLevelPath) {
        alert("请先加载一个 .adofai 关卡文件");
        return;
    }

    input.value = "";
    isLoading = true;
    const sendBtn = document.getElementById("send-btn");
    sendBtn.disabled = true;

    appendLoadingIndicator();

    try {
        const res = await fetch(`${API_BASE}/api/chat`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                session_id: currentSessionId,
                message: message
            })
        });
        const data = await res.json();

        removeLoadingIndicator();

        if (data.error) {
            alert("错误: " + data.error);
        } else {
            await loadMessages();
            if (data.level_info) {
                updateToolbar(data.level_info);
            }
            currentUndoCount = data.undo_count || 0;
            updateUndoButton();
        }
    } catch (e) {
        removeLoadingIndicator();
        console.error("发送消息失败:", e);
        alert("发送消息失败，请检查网络连接");
    }

    isLoading = false;
    sendBtn.disabled = false;
}

// ==================== 撤回 ====================
function updateUndoButton() {
    const btn = document.getElementById("btn-undo");
    btn.disabled = currentUndoCount <= 0;
    btn.textContent = `↩ 撤回 (${currentUndoCount})`;
}

async function undoLastOperation() {
    if (!currentSessionId || currentUndoCount <= 0) return;

    isLoading = true;
    appendLoadingIndicator();

    try {
        const res = await fetch(`${API_BASE}/api/undo/${currentSessionId}`, {
            method: "POST"
        });
        const data = await res.json();

        removeLoadingIndicator();

        if (data.undone) {
            currentUndoCount = data.remaining_undo || 0;
            updateUndoButton();
            await loadMessages();
        } else {
            alert(data.message || "撤回失败");
        }
    } catch (e) {
        removeLoadingIndicator();
        console.error("撤回失败:", e);
        alert("撤回操作失败");
    }

    isLoading = false;
}

// ==================== 关卡加载 ====================
function showLoadLevelModal() {
    if (!currentSessionId) {
        alert("请先创建或选择一个会话");
        return;
    }

    const overlay = document.createElement("div");
    overlay.className = "modal-overlay";
    overlay.id = "load-modal";
    overlay.innerHTML = `
        <div class="modal">
            <h3>加载 .adofai 关卡文件</h3>
            <div class="error-msg" id="load-error" style="display:none"></div>
            <label style="display:block;margin-bottom:4px;font-size:12px;color:var(--text-muted)">上传文件</label>
            <input type="file" id="load-file-input" accept=".adofai">
            <div style="text-align:center;margin:12px 0;color:var(--text-muted);font-size:12px">— 或 —</div>
            <label style="display:block;margin-bottom:4px;font-size:12px;color:var(--text-muted)">文件路径</label>
            <input type="text" id="load-path-input" placeholder="例：D:/levels/mylevel.adofai">
            <div class="modal-actions">
                <button class="btn" onclick="closeModal()">取消</button>
                <button class="btn btn-primary" id="btn-confirm-load">加载</button>
            </div>
        </div>`;
    document.body.appendChild(overlay);

    document.getElementById("btn-confirm-load").addEventListener("click", async () => {
        const fileInput = document.getElementById("load-file-input");
        const pathInput = document.getElementById("load-path-input");
        const errorEl = document.getElementById("load-error");

        const formData = new FormData();
        formData.append("session_id", currentSessionId);

        if (fileInput.files.length > 0) {
            formData.append("file", fileInput.files[0]);
        } else if (pathInput.value.trim()) {
            formData.append("file_path", pathInput.value.trim());
        } else {
            errorEl.style.display = "block";
            errorEl.textContent = "请选择文件或输入文件路径";
            return;
        }

        try {
            const res = await fetch(`${API_BASE}/api/load_level`, {
                method: "POST",
                body: formData
            });
            const data = await res.json();

            if (data.error) {
                errorEl.style.display = "block";
                errorEl.textContent = data.error;
            } else {
                currentLevelPath = data.level_info.file_path;
                updateToolbar(data.level_info);
                closeModal();
                await loadMessages();
            }
        } catch (e) {
            errorEl.style.display = "block";
            errorEl.textContent = "加载失败: " + e.message;
        }
    });
}

function closeModal() {
    const modal = document.getElementById("load-modal");
    if (modal) modal.remove();
}

function updateToolbar(levelInfo) {
    const el = document.getElementById("toolbar-level-info");
    if (!levelInfo || !currentLevelPath) {
        el.innerHTML = `<span class="label">未加载关卡</span>`;
        return;
    }

    const parts = [];
    if (levelInfo.song) parts.push(`🎵 ${levelInfo.song}`);
    if (levelInfo.artist) parts.push(`👤 ${levelInfo.artist}`);
    if (levelInfo.bpm) parts.push(`🎼 ${levelInfo.bpm} BPM`);
    parts.push(`🧱 ${levelInfo.tile_count || 0} tiles`);

    const fileName = currentLevelPath.split(/[/\\]/).pop();
    el.innerHTML = `
        <span class="label">已加载</span>
        <span class="value" title="${escapeHtml(currentLevelPath)}">${escapeHtml(fileName)}</span>
        <span style="margin-left:8px;color:var(--text-muted);font-size:11px">${parts.join(" · ")}</span>`;
}

// ==================== API Key 管理 ====================

async function checkApiKeyStatus() {
    try {
        const res = await fetch(`${API_BASE}/api/api_key_status`);
        const data = await res.json();
        updateApiKeyIndicator(data.configured);
    } catch (e) {
        console.error("检查 API Key 状态失败:", e);
    }
}

function updateApiKeyIndicator(configured) {
    const el = document.getElementById("api-key-indicator");
    if (configured) {
        el.innerHTML = '<span class="dot ok"></span> API Key';
        el.title = "DeepSeek API Key 已配置";
    } else {
        el.innerHTML = '<span class="dot missing"></span> API Key';
        el.title = "DeepSeek API Key 未配置，点击 ⚙ 设置";
    }
}

function showSettingsModal() {
    const modal = document.getElementById("settings-modal");
    const errorEl = document.getElementById("settings-error");
    const statusEl = document.getElementById("settings-key-status");
    errorEl.style.display = "none";
    const input = document.getElementById("settings-api-key-input");
    input.value = "";

    fetch(`${API_BASE}/api/api_key_status`).then(r => r.json()).then(data => {
        if (data.configured) {
            statusEl.innerHTML = "✅ API Key 已配置";
            input.placeholder = "输入新 Key 以替换当前配置";
        } else {
            statusEl.innerHTML = "❌ API Key 未配置，请输入你的 DeepSeek API Key";
            input.placeholder = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx";
        }
    }).catch(() => {
        statusEl.innerHTML = "❌ API Key 未配置";
    });

    modal.style.display = "flex";
}

function closeSettingsModal() {
    document.getElementById("settings-modal").style.display = "none";
    document.getElementById("settings-error").style.display = "none";
}

async function saveApiKey() {
    const input = document.getElementById("settings-api-key-input");
    const errorEl = document.getElementById("settings-error");
    const apiKey = input.value.trim();

    if (!apiKey) {
        errorEl.style.display = "block";
        errorEl.textContent = "请输入 API Key";
        return;
    }

    errorEl.style.display = "none";

    try {
        const res = await fetch(`${API_BASE}/api/set_api_key`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ api_key: apiKey })
        });
        const data = await res.json();

        if (data.error) {
            errorEl.style.display = "block";
            errorEl.textContent = data.error;
        } else {
            updateApiKeyIndicator(true);
            closeSettingsModal();
        }
    } catch (e) {
        errorEl.style.display = "block";
        errorEl.textContent = "保存失败: " + e.message;
    }
}

// 点击弹窗外部关闭
document.addEventListener("click", (e) => {
    const modal = document.getElementById("settings-modal");
    if (e.target === modal) {
        closeSettingsModal();
    }
});

// ==================== 简单 Markdown 渲染 ====================
function renderMarkdown(text) {
    if (!text) return "";
    let html = escapeHtml(text);

    // 代码块
    html = html.replace(/```(\w*)\n([\s\S]*?)```/g, (_, lang, code) => {
        return `<pre><code class="language-${lang || ''}">${escapeHtml(code.trim())}</code></pre>`;
    });

    // 行内代码
    html = html.replace(/`([^`]+)`/g, "<code>$1</code>");

    // 粗体
    html = html.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");

    // 斜体
    html = html.replace(/\*([^*]+)\*/g, "<em>$1</em>");

    // 列表项
    html = html.replace(/^- (.+)$/gm, "<li>$1</li>");
    html = html.replace(/((?:<li>.*<\/li>\n?)+)/g, "<ul>$1</ul>");

    // 换行
    html = html.replace(/\n/g, "<br>");

    return html;
}

function escapeHtml(text) {
    if (!text) return "";
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}
