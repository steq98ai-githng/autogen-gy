import pytest
from autogen_core import ComponentModel
from autogenstudio.gallery.builder import GalleryBuilder

def test_add_model():
    """Test adding a model component to the gallery builder."""
    builder = GalleryBuilder(id="test_gallery_id", name="Test Gallery")

    # Create a dummy model component
    dummy_model = ComponentModel(
        provider="autogen_ext.models.openai.OpenAIChatCompletionClient",
        component_type="model",
        version=1,
        component_version=1,
        description="A default model",
        label="Default Model",
        config={"model": "gpt-4o-mini"}
    )

    # Test adding a model with custom label and description
    custom_label = "Custom GPT-4o-mini"
    custom_desc = "Custom Description for GPT-4o-mini"
    result = builder.add_model(dummy_model, label=custom_label, description=custom_desc)

    # Assert builder chaining works
    assert result is builder

    # Assert model was added
    assert len(builder.models) == 1

    # Assert custom metadata was updated
    added_model = builder.models[0]
    assert added_model.label == custom_label
    assert added_model.description == custom_desc

    # Create another model to test default add behavior without optional params
    dummy_model_2 = ComponentModel(
        provider="autogen_ext.models.anthropic.AnthropicChatCompletionClient",
        component_type="model",
        version=1,
        component_version=1,
        description="Default Anthropic",
        label="Anthropic Claude",
        config={"model": "claude-3-7-sonnet-20250219"}
    )

    builder.add_model(dummy_model_2)

    # Assert second model was added and default metadata preserved
    assert len(builder.models) == 2
    added_model_2 = builder.models[1]
    assert added_model_2.label == "Anthropic Claude"
    assert added_model_2.description == "Default Anthropic"
