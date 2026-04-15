import autogen
import os

# 設定 LLM 配置 (JULES 執行時會自動帶入環境變數)
config_list = [{
    "model": "gemini-1.5-pro-preview-0409", # 或替換為你實際使用的模型
    "api_key": os.environ.get("GEMINI_API_KEY", "YOUR_API_KEY")
}]

llm_config = {"config_list": config_list, "cache_seed": 42}

def main():
    print("啟動 AutoGen 雙代理人審查系統...")

    # 建立「規劃與審查者」代理人 (Planning Critic)
    critic = autogen.AssistantAgent(
        name="Architecture_Critic",
        system_message="你是一位嚴格的軟體架構師。你的任務是審查程式碼、提出重構建議，並找出潛在的效能瓶頸。請給出具體的修改方案。",
        llm_config=llm_config,
    )

    # 建立「執行者」代理人 (相當於 JULES 的雙手)
    executor = autogen.UserProxyAgent(
        name="JULES_Executor",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=3,
        is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
        code_execution_config={
            "work_dir": "workspace",
            "use_docker": False, # 在 JULES 的 VM 中直接執行
        },
        system_message="你是一個代碼執行者。請根據 Critic 的建議撰寫 Python 代碼並執行。如果任務完成，請回覆 TERMINATE。"
    )

    # 啟動自動優化對話
    executor.initiate_chat(
        critic,
        message="請分析當前專案的結構，並寫出一段能自動掃描專案中所有 .py 檔案並列出複雜度過高函式的 Python 腳本。寫好後請讓我執行。"
    )

if __name__ == "__main__":
    main()
