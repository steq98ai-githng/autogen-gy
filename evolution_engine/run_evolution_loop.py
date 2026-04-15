# ================================================
# Jules IDE 專攻型 AutoGen 多代理自我學習進化系統
# 版本：v1.1 - 加入 Seed Knowledge 自動持久化閉環
# 作者：steq98ai
# ================================================

import autogen
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
import json
import os
from datetime import datetime
from typing import List, Dict, Any

# ====================== 檔案路徑 ======================
SEED_KNOWLEDGE_FILE = "jules_seed_knowledge.json"

# ====================== LLM 配置 ======================
config_list = [
    {
        "model": "gpt-4o",
        "api_key": "YOUR_API_KEY_HERE",   # ← 替換成您的 API Key
        "temperature": 0.3,
    }
]

llm_config = {"config_list": config_list, "timeout": 180}

# ====================== IDE 專攻核心規則 ======================
IDE_DOMINANT_RULE = """
**IDE 專攻型行為分布蒸餾規則（Dominant Objective Function）**：
1. 所有輸出必須優先強化「工程可實作性、模組化、可直接執行、IDE開發決策判斷」。
2. 除非涉及核心架構，否則禁止展開任何泛知識。
3. 必須將所有問題投影到「模組化重構 + 可執行腳本 + 開發決策」軸向。
4. 錯誤答案一律強制重寫成可直接在 IDE 中執行的模組化形式。
5. 最終輸出必須包含：明確步驟、可執行程式碼片段、模組化架構（文字版）。
這是 Projection Distillation 的核心，請嚴格遵守。
"""

# ====================== Seed Knowledge 持久化功能 ======================
def load_seed_knowledge() -> Dict:
    if os.path.exists(SEED_KNOWLEDGE_FILE):
        with open(SEED_KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            print(f"✅ 已載入 Seed Knowledge，共 {len(data.get('versions', []))} 個版本")
            return data
    else:
        initial_data = {
            "versions": [],
            "latest_version": None
        }
        save_seed_knowledge(initial_data)
        return initial_data

def save_seed_knowledge(data: Dict):
    with open(SEED_KNOWLEDGE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"💾 Seed Knowledge 已更新並持久化")

def append_to_seed_knowledge(new_knowledge: str, evaluation_score: float, task_description: str):
    data = load_seed_knowledge()
    
    version = {
        "timestamp": datetime.now().isoformat(),
        "task": task_description,
        "optimized_knowledge": new_knowledge.strip(),
        "evaluation_score": evaluation_score,
        "version_id": len(data["versions"]) + 1
    }
    
    data["versions"].append(version)
    data["latest_version"] = version
    
    save_seed_knowledge(data)
    print(f"🌱 新優化知識已寫入 Seed Knowledge (版本 {version['version_id']}, 分數: {evaluation_score:.1f})")

# ====================== Agent 建立函式 ======================
def create_ide_agent(name: str, system_message: str) -> AssistantAgent:
    return AssistantAgent(
        name=name,
        system_message=IDE_DOMINANT_RULE + "\n\n" + system_message,
        llm_config=llm_config,
    )

# ====================== 建立所有 Agent ======================
controller = create_ide_agent("Jules_Controller", "你是 Jules 核心控制器，負責 orchestrating 完整自我學習進化循環，並確保知識持久化。")

teacher = create_ide_agent("Teacher_LLM", "你是 Teacher LLM，負責知識引出（Sec. 3.1）。")
student = create_ide_agent("Student_Model", "你是 Student Model，負責知識蒸餾（Sec. 3.2）。")

labeling = create_ide_agent("Labeling_Agent", "Labeling Agent：輸入 → 產生 IDE 專攻型 label Y。")
expansion = create_ide_agent("Expansion_Agent", "Expansion Agent：擴展 demonstrations 成 X,Y 對，並強制 IDE 投影。")
data_curation = create_ide_agent("DataCuration_Agent", "Data Curation Agent：合成高品質 X,Y 對（Projection Distillation）。")
feature = create_ide_agent("Feature_Agent", "Feature Agent：提取 feature 供後續比較。")
feedback = create_ide_agent("Feedback_Agent", "Feedback Agent：雙向回饋並強制檢查排他條件。")
self_knowledge = create_ide_agent("SelfKnowledge_Agent", "Self-Knowledge Agent：產生 output 並自我審查可執行性。")

rank_optimizer = create_ide_agent("RankOptimizer_Agent", "Rank Optimization Agent：執行 y¹,y²,y³ 偏好排名。")
rl_agent = create_ide_agent("RL_Agent", "RL Agent：計算 reward 並進行 distil。")

evaluator = create_ide_agent(
    "Evaluator_Agent",
    """你是專攻曲線評估 Agent。
請比較初始版本與優化後版本，輸出以下格式（必須包含這幾行）：
- Engineering_Practicality_Score: XX/100
- Modularization_Score: XX/100
- Projection_Compliance: XX/100
- Overall_Improvement: XX/100
- Optimized_Knowledge: [這裡貼上最終優化後的最完整知識內容]
- Next_Suggestion: [下一步強化建議]
"""
)

# ====================== GroupChat 配置 ======================
agents: List[AssistantAgent] = [
    controller, teacher, student, labeling, expansion, data_curation,
    feature, feedback, self_knowledge, rank_optimizer, rl_agent, evaluator
]

groupchat = GroupChat(
    agents=agents,
    messages=[],
    max_round=35,
    speaker_selection_method="round_robin",
)

manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)

# ====================== User Proxy ======================
user_proxy = UserProxyAgent(
    name="User_Proxy",
    human_input_mode="NEVER",
    code_execution_config=False,
    is_termination_msg=lambda x: x.get("content", "").strip().endswith("TERMINATE"),
)

# ====================== 主執行流程 ======================
if __name__ == "__main__":
    # 載入最新 Seed Knowledge
    seed_data = load_seed_knowledge()
    latest_seed = seed_data["latest_version"]["optimized_knowledge"] if seed_data["latest_version"] else "初始空白 Seed Knowledge"

    test_task = """設計一個可自動化「多代理 IDE 開發流程」的 AutoGen 群聊架構，要求完全模組化、可直接執行、具備自我方向校正機制。"""

    print("🚀 Jules IDE 專攻型自我學習進化系統 v1.1 啟動（Seed Knowledge 持久化已開啟）")
    print("=" * 90)

    initial_message = f"""
目前 Seed Knowledge（最新版本）：
{latest_seed[:800]}...（已截斷）

本次測試任務：
{test_task}

請執行完整 Jules 自我學習進化循環：
1. Teacher LLM 知識引出
2. Student Model 蒸餾
3. 六大子模塊執行
4. Rank Optimization + RL distil
5. Evaluator 進行專攻曲線評估
6. 最後必須由 Controller 觸發將優化知識自動寫回 Seed Knowledge

嚴格遵守 IDE 專攻型 Dominant Objective Function。
請在 Evaluator 輸出後，以 "TERMINATE" 結束循環。
"""

    chat_history = user_proxy.initiate_chat(
        manager,
        message=initial_message
    )

    # ====================== 自動提取並持久化優化知識 ======================
    print("\n🔄 正在自動提取優化知識並寫回 Seed Knowledge...")

    # 從對話中找出 Evaluator 的最後輸出
    final_messages = groupchat.messages
    optimized_knowledge = "未成功提取"
    eval_score = 0.0

    for msg in reversed(final_messages):
        if msg.get("name") == "Evaluator_Agent":
            content = msg.get("content", "")
            if "Optimized_Knowledge:" in content:
                # 簡單解析（實際可改用更穩定的 parser）
                try:
                    parts = content.split("Optimized_Knowledge:")
                    if len(parts) > 1:
                        optimized_knowledge = parts[1].split("Next_Suggestion:")[0].strip()
                    
                    # 提取分數
                    if "Overall_Improvement:" in content:
                        score_line = [line for line in content.split("\n") if "Overall_Improvement" in line]
                        if score_line:
                            eval_score = float(score_line[0].split(":")[1].strip().split("/")[0])
                except:
                    pass
            break

    # 寫回 Seed Knowledge
    append_to_seed_knowledge(
        new_knowledge=optimized_knowledge,
        evaluation_score=eval_score,
        task_description=test_task
    )

    print("\n✅ Jules 完整閉環自我進化完成！")
    print(f"最新 Seed Knowledge 已持久化，總版本數：{len(seed_data['versions']) + 1}")
