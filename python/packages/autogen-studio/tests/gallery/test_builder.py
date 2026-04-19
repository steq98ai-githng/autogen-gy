import pytest
from autogenstudio.gallery.builder import GalleryBuilder

def test_set_metadata():
    builder = GalleryBuilder(id="test_id", name="test_name")

    # Check default metadata
    assert builder.metadata.author == "AutoGen Team"
    assert builder.metadata.version == "1.0.0"

    # Update metadata
    updated_builder = builder.set_metadata(
        author="New Author",
        version="2.0.0",
        description="A new description",
        tags=["tag1", "tag2"],
        license="Apache 2.0",
        category="test"
    )

    # Verify method chaining (returns self)
    assert updated_builder is builder

    # Verify metadata was updated
    assert builder.metadata.author == "New Author"
    assert builder.metadata.version == "2.0.0"
    assert builder.metadata.description == "A new description"
    assert builder.metadata.tags == ["tag1", "tag2"]
    assert builder.metadata.license == "Apache 2.0"
    assert builder.metadata.category == "test"

    # Verify partial update (other fields unchanged)
    builder.set_metadata(author="Third Author")
    assert builder.metadata.author == "Third Author"
    assert builder.metadata.version == "2.0.0" # Unchanged
