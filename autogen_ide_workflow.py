import asyncio
from autogen_agentchat.agents import AssistantAgent, CodeExecutorAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_ext.models.replay import ReplayChatCompletionClient
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor

async def main() -> None:
    # 1. Provide mock outputs for replay client
    client = ReplayChatCompletionClient(
        chat_completions=[
            "```python\nprint('hello world')\n```",
            "I reviewed the code and the execution output. It looks good. TERMINATE"
        ]
    )

    # 2. Define the agents
    developer = AssistantAgent(
        "Developer",
        model_client=client,
        system_message="你是一位資深軟體工程師。負責編寫高質量、模組化且可執行的Python代碼。請直接輸出代碼。"
    )

    reviewer = AssistantAgent(
        "Reviewer",
        model_client=client,
        system_message="你是代碼審查員。嚴格檢查代碼的模組化、可實作性與安全性。若有錯誤請提出具體修正建議。若審查通過，請輸出 TERMINATE。"
    )

    executor = CodeExecutorAgent(
        "Executor",
        code_executor=LocalCommandLineCodeExecutor(work_dir="workspace")
    )

    # 3. Create termination condition
    termination = TextMentionTermination("TERMINATE")

    # 4. Construct RoundRobinGroupChat
    team = RoundRobinGroupChat(
        [executor, developer, reviewer],
        termination_condition=termination
    )

    # 5. Execute task
    result = await team.run(task="請寫一個 hello world python script 並執行它。")
    print("Execution completed.")
    print("Messages:", len(result.messages))

if __name__ == "__main__":
    asyncio.run(main())
