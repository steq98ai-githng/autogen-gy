import os
import pytest
from unittest.mock import patch
from autogenstudio.cli import serve, lite

def test_serve_success():
    """Test the serve command with a valid team file."""
    team_file = "valid_team.json"
    host = "127.0.0.1"
    port = 8084
    workers = 1
    reload = False
    docs = False

    with patch("os.path.exists", return_value=True), \
         patch("uvicorn.run") as mock_run, \
         patch.dict(os.environ, {}, clear=False):

        serve(team=team_file, host=host, port=port, workers=workers, reload=reload, docs=docs)

        # Verify environment variables
        assert os.environ["AUTOGENSTUDIO_API_DOCS"] == str(docs)
        assert os.environ["AUTOGENSTUDIO_TEAM_FILE"] == team_file

        # Verify uvicorn.run call
        mock_run.assert_called_once_with(
            "autogenstudio.web.serve:app",
            host=host,
            port=port,
            workers=workers,
            reload=reload,
        )

def test_serve_file_not_found():
    """Test that serve raises ValueError when the team file does not exist."""
    team_file = "nonexistent_team.json"

    with patch("os.path.exists", return_value=False):
        with pytest.raises(ValueError, match=f"Team file not found: {team_file}"):
            serve(team=team_file)

def test_serve_custom_params():
    """Test the serve command with custom parameters."""
    team_file = "custom_team.json"
    host = "0.0.0.0"
    port = 9000
    workers = 4
    reload = True
    docs = True

    with patch("os.path.exists", return_value=True), \
         patch("uvicorn.run") as mock_run, \
         patch.dict(os.environ, {}, clear=False):

        serve(team=team_file, host=host, port=port, workers=workers, reload=reload, docs=docs)

        # Verify environment variables
        assert os.environ["AUTOGENSTUDIO_API_DOCS"] == str(docs)
        assert os.environ["AUTOGENSTUDIO_TEAM_FILE"] == team_file

        # Verify uvicorn.run call
        mock_run.assert_called_once_with(
            "autogenstudio.web.serve:app",
            host=host,
            port=port,
            workers=workers,
            reload=reload,
        )

def test_lite_default():
    """Test the lite command with default parameters."""
    with patch("autogenstudio.lite.LiteStudio") as mock_lite:
        mock_instance = mock_lite.return_value
        lite()

        mock_lite.assert_called_once_with(
            team=None,
            host="127.0.0.1",
            port=8080,
            auto_open=True,
            session_name="Lite Session"
        )
        mock_instance.start.assert_called_once()
        mock_instance.stop.assert_not_called()

def test_lite_custom_params():
    """Test the lite command with custom parameters."""
    team_file = "custom_team.json"
    host = "0.0.0.0"
    port = 9000
    auto_open = False
    session_name = "Custom Session"

    with patch("autogenstudio.lite.LiteStudio") as mock_lite:
        mock_instance = mock_lite.return_value
        lite(
            team=team_file,
            host=host,
            port=port,
            auto_open=auto_open,
            session_name=session_name
        )

        mock_lite.assert_called_once_with(
            team=team_file,
            host=host,
            port=port,
            auto_open=auto_open,
            session_name=session_name
        )
        mock_instance.start.assert_called_once()
        mock_instance.stop.assert_not_called()

def test_lite_keyboard_interrupt():
    """Test that the lite command handles KeyboardInterrupt correctly."""
    with patch("autogenstudio.lite.LiteStudio") as mock_lite:
        mock_instance = mock_lite.return_value
        # Make start() raise KeyboardInterrupt
        mock_instance.start.side_effect = KeyboardInterrupt()

        lite()

        mock_lite.assert_called_once()
        mock_instance.start.assert_called_once()
        # stop() should be called when KeyboardInterrupt is raised
        mock_instance.stop.assert_called_once()
