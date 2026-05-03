import asyncio
import datetime
import json
import logging
import os
from typing import Any, Dict

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import MaxMessageTermination, TextMessageTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_core.models import CreateResult, ModelInfo, RequestUsage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MockModelClient:
    """Mock Model Client implementing AutoGen >= 0.4.x expected structure."""

    def __init__(self, role: str = "assistant"):
        self.role = role

    async def create(self, messages: Any, **kwargs: Any) -> CreateResult:
        usage = RequestUsage(prompt_tokens=10, completion_tokens=10)
        return CreateResult(content="Here is the code. APPROVE", usage=usage, finish_reason="stop", cached=False)

    @property
    def model_info(self) -> ModelInfo:
        return ModelInfo(
            vision=False,
            function_calling=True,
            json_output=True,
            family="unknown",
            structured_output=True,
        )


class SeedKnowledgeManager:
    """Handles automatic persistence of Seed Knowledge."""

    def __init__(self, filepath: str):
        self.filepath = filepath
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)

    def load(self) -> Dict[str, Any]:
        """Loads seed knowledge from file or returns default structure if not found."""
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r") as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        data.setdefault("history", [])
                        data.setdefault("modules", [])
                        return data
            except (json.JSONDecodeError, IOError):
                pass
        return {"version": "v1.0", "summary": "Initial seed", "history": [], "modules": []}

    def save(self, data: Dict[str, Any]) -> None:
        """Saves seed knowledge to file."""
        with open(self.filepath, "w") as f:
            json.dump(data, f, indent=2)
        logger.info("Seed knowledge saved successfully.")


async def create_and_run_ide_loop(task: str, seed_knowledge: Dict[str, Any]) -> Dict[str, Any]:
    """
    Creates an AutoGen group chat for an automated IDE development loop.
    Focus: Modularity, Executability, Developer Decision Making.
    """
    model_client = MockModelClient()

    # Module 1: Coder Agent
    coder = AssistantAgent(
        name="Coder",
        model_client=model_client,
        description="You are a Coder. You write executable Python code to solve the task. Focus on modularity and executability. Return ONLY complete code blocks.",
        system_message="You are a Coder. You write executable Python code to solve the task. Focus on modularity and executability. Return ONLY complete code blocks.",
    )

    # Module 2: Reviewer Agent
    reviewer = AssistantAgent(
        name="Reviewer",
        model_client=model_client,
        description="You are a Reviewer. Check the code for IDE execution viability, modularity, and correctness. Provide actionable fixes. If correct, return 'APPROVE'.",
        system_message="You are a Reviewer. Check the code for IDE execution viability, modularity, and correctness. Provide actionable fixes. If correct, return 'APPROVE'.",
    )

    # Module 3: System Controller (Proxy replacement)
    system = AssistantAgent(
        name="System_Controller",
        model_client=model_client,
        description="You act as the IDE environment and system controller.",
        system_message="You act as the IDE environment and system controller. Check conditions and manage persistence.",
    )

    # Module 4: Group Chat Manager
    termination = TextMessageTermination("APPROVE") | MaxMessageTermination(5)
    team = RoundRobinGroupChat([system, coder, reviewer], termination_condition=termination)

    logger.info(f"Starting IDE Loop for task: {task}")
    result = await team.run(task=task)

    success = any(
        hasattr(msg, "content") and isinstance(msg.content, str) and "APPROVE" in msg.content for msg in result.messages
    )

    if success:
        logger.info("IDE Loop Executable Module Initialized and Ran Successfully.")
    else:
        logger.warning("IDE Loop failed to achieve 'APPROVE' state.")

    seed_knowledge["history"].append({"timestamp": str(datetime.datetime.now()), "task": task, "success": success})
    module_info = {
        "name": "IDE_GroupChat",
        "description": "Multi-agent loop containing Coder, Reviewer, and System_Controller",
    }
    if module_info not in seed_knowledge["modules"]:
        seed_knowledge["modules"].append(module_info)
    return seed_knowledge


async def main() -> None:
    date_str = datetime.datetime.now().strftime("%Y%m%d")
    filepath = f"knowledge_base/seed_knowledge_v{date_str}.json"
    knowledge_manager = SeedKnowledgeManager(filepath)
    seed_knowledge = knowledge_manager.load()

    task = "Design an automated multi-agent IDE development workflow AutoGen group chat architecture."
    try:
        updated_knowledge = await create_and_run_ide_loop(task, seed_knowledge)
        knowledge_manager.save(updated_knowledge)
        logger.info("Daily AI Evolution Loop completed successfully.")
    except Exception as e:
        logger.error(f"Error in IDE loop: {e}")


if __name__ == "__main__":
    asyncio.run(main())
