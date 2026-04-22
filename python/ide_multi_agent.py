"""
IDE Multi-Agent System Module
This script implements an automated AutoGen group chat architecture designed for IDE workflows.
"""

import asyncio
import os
import sys
import traceback
from typing import Optional

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_core.models import ModelInfo
from autogen_ext.models.openai import OpenAIChatCompletionClient

class MockChatCompletionClient(OpenAIChatCompletionClient):
    """Mock client for testing without actual API keys."""
    def __init__(self):
        super().__init__(
            model="gpt-4o-mini",
            api_key="mock",
            model_info=ModelInfo(
                vision=False,
                function_calling=True,
                json_output=True,
                family="unknown",
                structured_output=True,
            )
        )

    async def create(self, messages, **kwargs):
        from autogen_core.models import CreateResult
        from autogen_core.models import RequestUsage
        return CreateResult(
            finish_reason="stop",
            content="TERMINATE",
            usage=RequestUsage(prompt_tokens=10, completion_tokens=10),
            cached=False
        )


class IdeMultiAgentSystem:
    """Encapsulates the IDE multi-agent workflow."""

    def __init__(self, use_mock: bool = True):
        """Initialize the agent system and models."""
        self.use_mock = use_mock
        if use_mock:
            self.model_client = MockChatCompletionClient()
        else:
            api_key = os.environ.get("OPENAI_API_KEY", "mock")
            self.model_client = OpenAIChatCompletionClient(
                model="gpt-4o-mini",
                api_key=api_key,
                model_info=ModelInfo(
                    vision=False,
                    function_calling=True,
                    json_output=True,
                    family="gpt-4o-mini",
                    structured_output=True,
                )
            )

        self._setup_agents()
        self._setup_team()

    def _setup_agents(self):
        """Initialize the developer and reviewer agents."""
        self.developer = AssistantAgent(
            name="Developer",
            model_client=self.model_client,
            description="An expert software engineer who writes robust, modular code.",
            system_message="You are an expert developer. Output only the requested code block. If the task is done, reply with 'TERMINATE'."
        )

        self.reviewer = AssistantAgent(
            name="Reviewer",
            model_client=self.model_client,
            description="A strict code reviewer focusing on execution stability.",
            system_message="Review the code. If there are no issues, reply with 'TERMINATE'."
        )

    def _setup_team(self):
        """Configure the RoundRobinGroupChat."""
        text_termination = TextMentionTermination("TERMINATE")
        max_msg_termination = MaxMessageTermination(max_messages=5)
        termination = text_termination | max_msg_termination

        self.team = RoundRobinGroupChat(
            participants=[self.developer, self.reviewer],
            termination_condition=termination
        )

    async def run_task(self, task: str):
        """Execute the workflow asynchronously."""
        try:
            print(f"Starting IDE task: {task}")
            # Ensure task output is awaited and printed to console
            stream = self.team.run_stream(task=task)
            await Console(stream)
            print("Task completed successfully.")
            return True
        except Exception as e:
            print(f"Task failed with error: {e}", file=sys.stderr)
            traceback.print_exc()
            return False


async def main():
    """Main execution point for direct testing."""
    ide_system = IdeMultiAgentSystem(use_mock=True)
    task_desc = "Write a basic hello world script."
    success = await ide_system.run_task(task_desc)

    if not success:
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
