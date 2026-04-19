import pytest
from autogenstudio.gallery.builder import GalleryBuilder
from autogen_agentchat.conditions import TextMentionTermination

def test_add_termination():
    builder = GalleryBuilder(id="test_gallery", name="Test Gallery")

    # Create a termination component
    termination = TextMentionTermination(text="TERMINATE")
    termination_component = termination.dump_component()

    # Add termination without label/description
    result = builder.add_termination(termination_component)

    # Check that builder returns itself (fluent interface)
    assert result is builder

    # Check that it was added to the terminations list
    assert len(builder.terminations) == 1
    assert builder.terminations[0] == termination_component

    # Add termination with label and description
    termination2 = TextMentionTermination(text="STOP")
    termination_component2 = termination2.dump_component()

    builder.add_termination(
        termination_component2,
        label="Stop Termination",
        description="Terminates on STOP"
    )

    assert len(builder.terminations) == 2
    # Verify metadata was updated
    assert getattr(builder.terminations[1], "label", None) == "Stop Termination"
    assert getattr(builder.terminations[1], "description", None) == "Terminates on STOP"
