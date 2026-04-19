import pytest
from autogenstudio.gallery.builder import GalleryBuilder

def test_set_metadata():
    builder = GalleryBuilder(id="test_id", name="test_gallery")

    # Test setting some metadata
    builder.set_metadata(
        author="Test Author",
        version="2.0.0",
        description="A test description"
    )

    assert builder.metadata.author == "Test Author"
    assert builder.metadata.version == "2.0.0"
    assert builder.metadata.description == "A test description"
    # Defaults should remain
    assert builder.metadata.license == "MIT"

    # Test setting the rest of metadata
    builder.set_metadata(
        tags=["test", "gallery"],
        license="Apache 2.0",
        category="testing"
    )

    assert builder.metadata.tags == ["test", "gallery"]
    assert builder.metadata.license == "Apache 2.0"
    assert builder.metadata.category == "testing"

    # Ensure previous ones are not overwritten if not passed
    assert builder.metadata.author == "Test Author"
    assert builder.metadata.version == "2.0.0"

    # Check chaining behavior
    builder2 = builder.set_metadata(version="3.0.0").set_metadata(author="Chained Author")
    assert builder2 is builder
    assert builder.metadata.version == "3.0.0"
    assert builder.metadata.author == "Chained Author"
