import os
import pytest
from unittest.mock import patch
from autogenstudio.cli import serve, get_env_file_path

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


def test_get_env_file_path_exists():
    """Test get_env_file_path when the .autogenstudio directory already exists."""
    with patch("os.path.expanduser", return_value="/mock/user/dir"), \
         patch("os.path.exists", return_value=True), \
         patch("os.makedirs") as mock_makedirs:

        env_file_path = get_env_file_path()

        assert env_file_path == os.path.join("/mock/user/dir", ".autogenstudio", "temp_env_vars.env")
        mock_makedirs.assert_not_called()


def test_get_env_file_path_not_exists():
    """Test get_env_file_path when the .autogenstudio directory does not exist."""
    with patch("os.path.expanduser", return_value="/mock/user/dir"), \
         patch("os.path.exists", return_value=False), \
         patch("os.makedirs") as mock_makedirs:

        env_file_path = get_env_file_path()

        app_dir = os.path.join("/mock/user/dir", ".autogenstudio")
        assert env_file_path == os.path.join(app_dir, "temp_env_vars.env")
        mock_makedirs.assert_called_once_with(app_dir, exist_ok=True)
