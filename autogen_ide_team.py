import asyncio
import logging
from typing import Any, AsyncGenerator, List, Union

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_core.models import (
    ChatCompletionClient,
    CreateResult,
    ModelCapabilities,
    ModelInfo,
    RequestUsage,
)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class MockChatCompletionClient(ChatCompletionClient):
    """
    Mock client to run tests without OpenAI API key.
    Ensures termination strings are output to prevent infinite loops.
    """
    def __init__(self):
        self.call_count = 0

    @property
    def model_info(self) -> ModelInfo:
        return ModelInfo(
            vision=False,
            function_calling=True,
            json_output=True,
            family="mock-model"
        )

    @property
    def capabilities(self) -> ModelCapabilities:
        return ModelCapabilities(
            vision=False,
            function_calling=True,
            json_output=True
        )

    async def create(self, messages: List[Any], **kwargs: Any) -> CreateResult:
        self.call_count += 1
        content = "Here is the implemented module."
        if self.call_count > 1:
            content = "LGTM. TERMINATE"

        return CreateResult(
            finish_reason="stop",
            content=content,
            usage=RequestUsage(prompt_tokens=10, completion_tokens=10),
            cached=False,
        )

    async def create_stream(self, messages: List[Any], **kwargs: Any) -> AsyncGenerator[Union[str, CreateResult], None]:
        self.call_count += 1
        content = "Here is the implemented module."
        if self.call_count > 1:
            content = "LGTM. TERMINATE"

        yield content
        yield CreateResult(
            finish_reason="stop",
            content=content,
            usage=RequestUsage(prompt_tokens=10, completion_tokens=10),
            cached=False,
        )

    async def close(self) -> None:
        pass

    def actual_usage(self) -> RequestUsage:
        return RequestUsage(prompt_tokens=10 * self.call_count, completion_tokens=10 * self.call_count)

    def total_usage(self) -> RequestUsage:
        return self.actual_usage()

    def count_tokens(self, messages: List[Any], **kwargs: Any) -> int:
        return 10

    def remaining_tokens(self) -> int:
        return 10000

async def main():
    """
    Main function to execute the automated multi-agent IDE development workflow.
    Sets up the team, runs the task, and returns the result.
    """
    model_client = MockChatCompletionClient()

    coder = AssistantAgent(
        name="Coder",
        description="A software engineer who writes and refactors code in the IDE.",
        system_message="You are a skilled software engineer. You write modular, clean code. When finished, output TERMINATE.",
        model_client=model_client,
    )

    reviewer = AssistantAgent(
        name="Reviewer",
        description="A code reviewer who evaluates the code for IDE compatibility and modularity.",
        system_message="You are a strict code reviewer. Evaluate the code. If acceptable, output TERMINATE.",
        model_client=model_client,
    )

    # Termination conditions: either reaching max messages or receiving the TERMINATE string
    text_termination = TextMentionTermination("TERMINATE")
    max_msgs = MaxMessageTermination(4)
    termination = text_termination | max_msgs

    # Create Group Chat with RoundRobin
    ide_team = RoundRobinGroupChat(
        participants=[coder, reviewer],
        termination_condition=termination,
    )

    task = "Design an automated multi-agent IDE development workflow AutoGen group chat architecture."
    logger.info(f"Starting workflow for task: {task}")

    result = await ide_team.run(task=task)

    logger.info("Workflow Results:")
    for msg in result.messages:
        logger.info(f"[{msg.source}]: {msg.content}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
