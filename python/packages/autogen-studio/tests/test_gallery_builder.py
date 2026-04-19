import pytest
from autogenstudio.gallery.builder import GalleryBuilder
from autogen_core import ComponentModel

def test_add_tool():
    builder = GalleryBuilder(id="test_gallery", name="Test Gallery")

    # Create a mock tool component
    tool = ComponentModel(
        provider="test_provider",
        component_type="tool",
        version=1,
        component_version=1,
        description="A test tool",
        label="Test Tool",
        config={"test": "config"}
    )

    # Test adding a tool without custom label and description
    builder.add_tool(tool)
    assert len(builder.tools) == 1
    assert builder.tools[0].label == "Test Tool"
    assert builder.tools[0].description == "A test tool"

    # Test adding a tool with custom label and description
    builder.add_tool(tool, label="Custom Label", description="Custom Description")
    assert len(builder.tools) == 2
    assert builder.tools[1].label == "Custom Label"
    assert builder.tools[1].description == "Custom Description"
    assert builder.tools[1].provider == "test_provider"
    assert builder.tools[1].component_type == "tool"
