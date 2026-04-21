from autogen_core import ComponentModel

from autogenstudio.gallery.builder import GalleryBuilder


def test_add_agent():
    # Create a builder instance
    builder = GalleryBuilder(id="test_gallery", name="Test Gallery")

    # Create a mock ComponentModel
    agent_component = ComponentModel(
        provider="autogen_agentchat.agents.AssistantAgent",
        component_type="agent",
        version=1,
        component_version=1,
        description="A test agent",
        label="Test Agent",
        config={
            "name": "test_agent",
            "model_client": {
                "provider": "autogen_ext.models.openai.OpenAIChatCompletionClient",
                "component_type": "model",
                "version": 1,
                "component_version": 1,
                "config": {"model": "gpt-4o-mini"},
            },
        },
    )

    # Add agent to builder
    builder.add_agent(agent_component)

    # Assert agent was added
    assert len(builder.agents) == 1
    assert builder.agents[0] == agent_component
    assert builder.agents[0].label == "Test Agent"
    assert builder.agents[0].description == "A test agent"

    # Test with custom label and description overrides
    agent_component2 = ComponentModel(
        provider="autogen_agentchat.agents.AssistantAgent",
        component_type="agent",
        version=1,
        component_version=1,
        description="Another test agent",
        label="Another Test Agent",
        config={"name": "test_agent2"},
    )

    # Add second agent with overrides
    builder.add_agent(agent_component2, label="Custom Label", description="Custom Description")

    # Assert agent was added with overrides
    assert len(builder.agents) == 2
    assert builder.agents[1] == agent_component2
    assert builder.agents[1].label == "Custom Label"
    assert builder.agents[1].description == "Custom Description"


def test_builder_chaining():
    # Create a builder instance
    builder = GalleryBuilder(id="test_gallery_chain", name="Test Gallery Chain")

    # Create a mock ComponentModel
    agent_component = ComponentModel(
        provider="autogen_agentchat.agents.AssistantAgent",
        component_type="agent",
        version=1,
        component_version=1,
        description="A test agent",
        label="Test Agent",
        config={"name": "test_agent"},
    )

    # Test that add_agent returns self (for method chaining)
    result = builder.add_agent(agent_component)
    assert result is builder
