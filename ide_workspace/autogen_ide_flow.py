import asyncio
from typing import AsyncGenerator
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.ui import Console
from autogen_core.models import CreateResult, RequestUsage, ChatCompletionClient, ModelCapabilities

class MockChatCompletionClient(ChatCompletionClient):
    """
    Mock chat completion client for local testing without network access.
    """
    def __init__(self, **kwargs):
        self.message_count = 0

    @property
    def model_info(self):
        return {
            "vision": False,
            "function_calling": False,
            "json_output": False,
            "family": "mock",
            "structured_output": False
        }

    @property
    def capabilities(self) -> ModelCapabilities:
        return ModelCapabilities(
            vision=False,
            function_calling=False,
            json_output=False
        )

    async def create(self, messages, **kwargs) -> CreateResult:
        self.message_count += 1
        usage = RequestUsage(prompt_tokens=10, completion_tokens=10)

        # Simulate conversation flow
        if self.message_count == 1:
            content = "Here is the factorial function:\n```python\ndef factorial(n):\n    if not isinstance(n, int) or n < 0:\n        raise ValueError('n must be a non-negative integer')\n    return 1 if n == 0 else n * factorial(n - 1)\n```"
        else:
            content = "APPROVE"

        return CreateResult(finish_reason="stop", content=content, usage=usage, cached=False)

    async def create_stream(self, messages, **kwargs) -> AsyncGenerator[str | CreateResult, None]:
        # Simple stream mock that yields the same content as create
        result = await self.create(messages, **kwargs)
        if isinstance(result.content, str):
            yield result.content
        yield result

    async def close(self) -> None:
        pass

    @property
    def actual_usage(self) -> RequestUsage:
        return RequestUsage(prompt_tokens=10, completion_tokens=10)

    @property
    def total_usage(self) -> RequestUsage:
        return RequestUsage(prompt_tokens=10, completion_tokens=10)

    def count_tokens(self, messages, tools=None):
        return 10

    def remaining_tokens(self, messages, tools=None):
        return 1000


class IDEWorkflowManager:
    """
    Manages a multi-agent IDE workflow using AutoGen AgentChat and an OpenAI model.
    """
    def __init__(self, use_mock=True):
        if use_mock:
            self.model_client = MockChatCompletionClient()
        else:
            self.model_client = OpenAIChatCompletionClient(model="gpt-4o")
        self._setup_agents()

    def _setup_agents(self):
        """Initializes the required agents for the workflow."""
        self.developer = AssistantAgent(
            name="Developer",
            model_client=self.model_client,
            description="Software engineer that writes code, debugs, and makes architectural decisions.",
            system_message="You are a skilled software developer. Your task is to write clean, modular, and executable Python code."
        )

        self.reviewer = AssistantAgent(
            name="Reviewer",
            model_client=self.model_client,
            description="Code reviewer that checks for modularity, execution issues, and bugs.",
            system_message="You are a strict code reviewer. Check the code provided by the Developer. If it looks perfect and requires no changes, reply with 'APPROVE'. Otherwise, suggest specific changes."
        )

        # Set up termination conditions: stop if 5 messages are reached or if 'APPROVE' is mentioned
        self.termination_condition = MaxMessageTermination(5) | TextMentionTermination("APPROVE")

        self.team = RoundRobinGroupChat(
            [self.developer, self.reviewer],
            termination_condition=self.termination_condition
        )

    async def run_workflow(self, task: str):
        """Runs the multi-agent workflow on a given task."""
        print(f"Starting IDE Workflow for task: {task}\n")

        # Use Console to visualize the conversation
        await Console(self.team.run_stream(task=task))


async def main():
    manager = IDEWorkflowManager(use_mock=True)
    # A simple task for demonstration
    task = "Write a modular Python function that computes the factorial of a number using recursion, including basic error handling."
    await manager.run_workflow(task)

if __name__ == "__main__":
    asyncio.run(main())
