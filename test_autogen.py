import asyncio
from typing import Sequence, List
import json
import os
from datetime import datetime

from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_core.models import ModelInfo, RequestUsage, CreateResult, ChatCompletionClient
from autogen_core.messages import ChatMessage, SystemMessage

class MockIDEClient(ChatCompletionClient):
    @property
    def model_info(self) -> ModelInfo:
        return ModelInfo(
            vision=False,
            function_calling=True,
            json_output=True,
            family="mock-ide-model",
            structured_output=True
        )

    async def create(self, messages: Sequence[ChatMessage], **kwargs) -> CreateResult:
        return CreateResult(
            content="Code generation completed. TERMINATE",
            usage=RequestUsage(prompt_tokens=10, completion_tokens=10),
            finish_reason="stop",
            cached=False
        )

    def actual_create_stream(self, messages: Sequence[ChatMessage], **kwargs):
        raise NotImplementedError()

    def count_tokens(self, messages: Sequence[ChatMessage], **kwargs) -> int:
        return 10

    def remaining_tokens(self, messages: Sequence[ChatMessage], **kwargs) -> int:
        return 1000

async def main():
    model_client = MockIDEClient()

    coder = AssistantAgent(
        name="Coder",
        model_client=model_client,
        system_message="You are a senior developer. Write modular code. End with TERMINATE."
    )

    reviewer = AssistantAgent(
        name="Reviewer",
        model_client=model_client,
        system_message="You review code for IDE compatibility."
    )

    user_proxy = UserProxyAgent(
        name="UserProxy",
        description="Executes code and provides feedback."
    )

    termination = MaxMessageTermination(3)
    team = RoundRobinGroupChat(
        participants=[coder, reviewer, user_proxy],
        termination_condition=termination
    )

    # Run the team
    # Wait, team.run requires a task string or messages
    try:
        # In autogen >= 0.4.x, we await team.run(task="...")
        result = await team.run(task="Design a module for file IO.")
        print(f"Task finished. Messages: len={len(result.messages)}")
    except Exception as e:
        print(f"Error running team: {e}")

if __name__ == "__main__":
    asyncio.run(main())
