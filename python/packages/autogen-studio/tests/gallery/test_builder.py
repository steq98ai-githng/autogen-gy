import pytest
from autogen_core import ComponentModel
from autogenstudio.gallery.builder import GalleryBuilder

def test_update_component_metadata():
    builder = GalleryBuilder(id="test_gallery", name="Test Gallery")

    # Create a mock component
    component = ComponentModel(
        provider="test_provider",
        component_type="agent",
        version=1,
        component_version=1,
        description="Original description",
        label="Original label",
        config={},
    )

    # Test updating both label and description
    updated_component = builder._update_component_metadata(
        component, label="New label", description="New description"
    )

    assert updated_component.label == "New label"
    assert updated_component.description == "New description"

    # Test updating only label
    updated_component = builder._update_component_metadata(component, label="Another label")
    assert updated_component.label == "Another label"
    assert updated_component.description == "New description" # Unchanged from previous step

    # Test updating only description
    updated_component = builder._update_component_metadata(component, description="Another description")
    assert updated_component.label == "Another label" # Unchanged
    assert updated_component.description == "Another description"

    # Test updating neither
    updated_component = builder._update_component_metadata(component)
    assert updated_component.label == "Another label" # Unchanged
    assert updated_component.description == "Another description" # Unchanged
