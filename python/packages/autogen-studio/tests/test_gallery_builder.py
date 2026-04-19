import pytest
from autogen_core import ComponentModel
from autogenstudio.gallery.builder import GalleryBuilder

def test_add_workbench():
    builder = GalleryBuilder(id="test_gallery_id", name="Test Gallery")

    # Create a mock component model
    mock_workbench = ComponentModel(
        provider="test_provider",
        component_type="workbench",
        version=1,
        component_version=1,
        description="Original description",
        label="Original label",
        config={"key": "value"}
    )

    # 1. Test adding without overrides
    # Test that it returns self to allow method chaining
    result = builder.add_workbench(mock_workbench)
    assert result is builder

    # Verify it was added correctly
    assert len(builder.workbenches) == 1
    assert builder.workbenches[0] == mock_workbench
    assert builder.workbenches[0].label == "Original label"
    assert builder.workbenches[0].description == "Original description"

    # Create another mock component
    mock_workbench2 = ComponentModel(
        provider="test_provider",
        component_type="workbench",
        version=1,
        component_version=1,
        description="Another original description",
        label="Another original label",
        config={"key2": "value2"}
    )

    # 2. Test adding with overrides
    builder.add_workbench(
        mock_workbench2,
        label="Overridden label",
        description="Overridden description"
    )

    # Verify it was added
    assert len(builder.workbenches) == 2

    # Verify the overrides were applied
    assert builder.workbenches[1].label == "Overridden label"
    assert builder.workbenches[1].description == "Overridden description"

    # Also verify that when partial overrides are passed, only those are updated
    mock_workbench3 = ComponentModel(
        provider="test_provider",
        component_type="workbench",
        version=1,
        component_version=1,
        description="Third original description",
        label="Third original label",
        config={"key3": "value3"}
    )

    builder.add_workbench(mock_workbench3, label="Only new label")
    assert len(builder.workbenches) == 3
    assert builder.workbenches[2].label == "Only new label"
    assert builder.workbenches[2].description == "Third original description"
