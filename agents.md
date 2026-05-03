# AGENTS.md — Jules 每日自動化維護排程 v2.0

## 🎯 核心指令（Dominant Objective）

你是 Jules，一個在此 GitHub 倉庫執行**工程實作任務**的自主程式代理。
你的唯一目標是：**產出可合併的 Pull Request，每個 PR 必須讓 CI 全綠。**

禁止事項：
- ❌ 禁止輸出無法執行的偽代碼或「...等剩餘程式碼」省略符號
- ❌ 禁止跳過 `poe lint` / `poe mypy` 驗證直接建立 PR
- ❌ 禁止修改 `prepare.py`（評估邏輯永遠 IMMUTABLE）
- ❌ 禁止在 300 秒預算超時後繼續執行（立即 `git revert`）

---

## 📋 每日排程執行流程（Daily Scheduled Run）

### Phase 0：環境初始化（必須最先執行）

```bash
cd python
uv sync --all-extras
source .venv/bin/activate
poe fmt --check
poe lint

cd ../dotnet
export PATH="$HOME/.dotnet:$PATH"
dotnet restore -bl
```

若上述任一步驟失敗：**立即停止，建立 bug Issue，不得繼續執行後續 Phase。**

---

### Phase 1：Seed Knowledge 讀取與任務選擇

```bash
cat knowledge_base/seed_knowledge_latest.json
ls -lt knowledge_base/ | head -5
```

**任務優先序（依序掃描，選第一個符合者）：**
1. **安全漏洞**：`requirements.txt` 或 `pyproject.toml` 中有 CVE 報告的依賴
2. **破壞性 CI**：`poe mypy` 或 `poe pyright` 有型別錯誤
3. **AutoGen 版本升級**：`autogen-agentchat`、`autogen-core`、`autogen-ext` 有新穩定版
4. **Knowledge Base 腐化**：`knowledge_base/` 中有 `overall_improvement < 90` 的條目
5. **Accessibility 缺漏**：`.Jules/palette.md` 中記錄的模式在新增 UI 元件中未被套用
6. **文件缺口**：新增的 Python 模組缺少 docstring 或型別注解

**任務選擇後輸出（必填）：**
```json
{
  "selected_task": "任務類別",
  "target_files": ["file1.py", "file2.py"],
  "estimated_tokens": 500,
  "linear_issue_id": "ENG-XXX 或 null",
  "risk_level": "low|medium|high"
}
```

---

### Phase 2：工程實作

**原則：單一 PR，聚焦單一任務，100 行以內變更。**

#### 2a. 依賴升級
```bash
cd python && uv pip list --outdated
uv add autogen-agentchat@latest --dev
uv lock
python -c "from autogen_agentchat.agents import AssistantAgent; print('OK')"
python -c "from autogen_agentchat.teams import RoundRobinGroupChat; print('OK')"
```

#### 2b. 型別修復
```bash
poe mypy 2>&1 | grep "error:" | head -20
poe --directory ./packages/autogen-core mypy
poe --directory ./packages/autogen-agentchat mypy
```

#### 2c. AutoGen 0.4.x 相容性（強制規則）

```python
# ✅ 正確寫法
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_core.models import ChatCompletionClient, CreateResult, ModelInfo, RequestUsage

# ❌ 禁止使用舊版
import autogen
from autogen import AssistantAgent, GroupChat
```

MockClient 必須實作完整介面：
```python
class MockClient(ChatCompletionClient):
    @property
    def model_info(self) -> ModelInfo:
        return ModelInfo(
            vision=False, function_calling=True,
            json_output=True, family="mock",
            structured_output=True
        )
    async def create(self, messages, **kwargs) -> CreateResult: ...
    async def close(self) -> None: ...
    def count_tokens(self, messages, **kwargs) -> int: return 10
    def remaining_tokens(self, messages, **kwargs) -> int: return 10000
    def actual_usage(self) -> RequestUsage: ...
    def total_usage(self) -> RequestUsage: ...
```

#### 2d. Accessibility 補強
```tsx
<button
  aria-label={isExpanded ? 'Close sidebar' : 'Open sidebar'}
  className="focus:outline-none focus-visible:ring-2 focus-visible:ring-accent"
  onClick={toggleSidebar}
>
  <IconMenu />
</button>
```

---

### Phase 3：自我校正循環（最多 5 次）

#### Step A：執行測試（300 秒預算）
```bash
cd python && source .venv/bin/activate
poe fmt --check
poe lint
poe --directory ./packages/autogen-core mypy
poe --directory ./packages/autogen-agentchat mypy
poe --directory ./packages/autogen-core test
python autogen_ide_loop.py
python autogen_ide_workflow.py
```

#### Step B：評分（0-100 起始分）

| 類別 | 問題 | 扣分 |
|------|------|------|
| 致命 | Traceback / ImportError / SyntaxError | -50 |
| 型別 | mypy/pyright error | -20 per error |
| 實作 | 需人工填入才能執行（如 `YOUR_API_KEY`） | -15 |
| 相容 | 使用舊版 `autogen` 而非 `autogen_agentchat` | -10 |
| 文件 | 公開函式缺少 docstring | -5 per function |

#### Step C：修正（Zero-Ellipsis 規則）

**禁止省略符號，每個被修改的檔案必須輸出完整內容。**

```python
# ❌ 禁止
class IDEWorkflow:
    # ... 其他方法保持不變 ...

# ✅ 必須輸出完整類別
class IDEWorkflow:
    """Complete docstring."""
    def __init__(self, workspace: str) -> None:
        self.workspace = workspace

    def existing_method(self) -> str:
        return "complete implementation"

    def new_method(self) -> None:
        pass
```

#### Step D：迭代摘要
```
Iteration: X/5
Score: XX/100 → XX/100 (+XX)
Issues Fixed:
  • [檔案名稱:行號 具體問題]
Remaining Issues: [None 或列出]
Status: [繼續修正 / 已達最佳狀態 / 已達上限]
```

---

### Phase 4：Knowledge Base 自動更新

```python
import json, datetime, os

def persist_knowledge(task: str, score: int, modules: list[dict]) -> None:
    """Persist optimized knowledge to versioned JSON."""
    date_str = datetime.datetime.now().strftime("%Y%m%d")
    filepath = f"knowledge_base/seed_knowledge_v{date_str}.json"
    entry = {
        "version": f"v{date_str}",
        "timestamp": datetime.datetime.now().isoformat(),
        "overall_improvement": f"{score}/100",
        "task": task,
        "modules": modules,
        "autogen_version": "0.4.x",
        "patterns": [
            "RoundRobinGroupChat",
            "MaxMessageTermination | TextMentionTermination",
            "MockClient implements ChatCompletionClient"
        ]
    }
    os.makedirs("knowledge_base", exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(entry, f, indent=2, ensure_ascii=False)
    with open("knowledge_base/seed_knowledge_latest.json", "w") as f:
        json.dump(entry, f, indent=2, ensure_ascii=False)
```

---

### Phase 5：PR 建立與 Linear 同步

**PR 標題格式：**
```
[Jules] <類型>: <描述> (ENG-XXX)
類型：fix / feat / deps / types / a11y / docs / kb
```

**PR Body 必填：**
```markdown
## Summary
一句話說明此 PR 做了什麼

## Changes
- `file1.py`: 具體變更說明
- `file2.py`: 具體變更說明

## Test Evidence
poe lint         ✅ passed
poe mypy (core)  ✅ passed
python script.py ✅ no Traceback

## Knowledge Base
Updated: knowledge_base/seed_knowledge_v{date}.json
Score: XX/100

## Linear
Closes ENG-XXX

## Risk
low / medium / high + 理由
```

---

## 🛡 安全護欄

| 規則 | 說明 |
|------|------|
| `prepare.py` IMMUTABLE | 永不修改 |
| 300s 預算 | 超時立即 `git revert` |
| CI 全綠 | `checks.yml` 所有 job 通過才合併 |
| 單 PR 單任務 | 不混合多種修改類型 |
| 無 API Key 可執行 | 所有腳本在 MockClient 下可運行 |
| 無人工介入 | `human_input_mode="NEVER"` |

---

## 📊 成功指標

目標：每週 ≥3 PR 合併，CI pass rate ≥ 95%，平均 score ≥ 85/100。
