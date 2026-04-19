import pytest
from autogenstudio.gallery.builder import GalleryBuilder
from autogen_core import ComponentModel

def test_add_team():
    # Setup
    builder = GalleryBuilder(id="test-gallery", name="Test Gallery")

    # Create a dummy component model
    team = ComponentModel(
        provider="test-provider",
        component_type="team",
        version=1,
        component_version=1,
        description="Test team description",
        label="Test Team",
        config={"key": "value"}
    )

    # Execute
    result = builder.add_team(team, label="Custom Label", description="Custom Description")

    # Assert
    assert result is builder  # Should return self for chaining
    assert len(builder.teams) == 1
    assert builder.teams[0] is team
    assert builder.teams[0].label == "Custom Label"
    assert builder.teams[0].description == "Custom Description"

def test_add_team_without_label_and_description():
    # Setup
    builder = GalleryBuilder(id="test-gallery", name="Test Gallery")

    # Create a dummy component model
    team = ComponentModel(
        provider="test-provider",
        component_type="team",
        version=1,
        component_version=1,
        description="Original description",
        label="Original Label",
        config={"key": "value"}
    )

    # Execute
    result = builder.add_team(team)

    # Assert
    assert result is builder
    assert len(builder.teams) == 1
    assert builder.teams[0] is team
    assert builder.teams[0].label == "Original Label"
    assert builder.teams[0].description == "Original description"
