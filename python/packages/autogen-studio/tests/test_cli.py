import os
import pytest
from unittest.mock import patch
from autogenstudio.cli import serve
from autogenstudio.cli import ui
import typer

def test_serve_success():
    """Test the serve command with a valid team file."""
    team_file = "valid_team.json"
    host = "127.0.0.1"
    port = 8084
    workers = 1
    reload = False
    docs = False

    with patch("autogenstudio.cli.os.path.exists", return_value=True), \
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

    with patch("autogenstudio.cli.os.path.exists", return_value=False):
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

    with patch("autogenstudio.cli.os.path.exists", return_value=True), \
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


def test_ui_success():
    """Test the ui command with default parameters."""
    with patch("autogenstudio.cli.get_env_file_path", return_value="/mock/path/temp_env_vars.env"), \
         patch("builtins.open") as mock_open, \
         patch("uvicorn.run") as mock_run:

        ui()

        # Verify get_env_file_path was called and open was used
        mock_open.assert_called_once_with("/mock/path/temp_env_vars.env", "w")

        # Verify the file was written to

        # Verify uvicorn.run call
        mock_run.assert_called_once_with(
            "autogenstudio.web.app:app",
            host="127.0.0.1",
            port=8081,
            workers=1,
            reload=False,
            reload_excludes=None,
            env_file="/mock/path/temp_env_vars.env",
        )

def test_ui_custom_params():
    """Test the ui command with custom parameters."""
    with patch("autogenstudio.cli.get_env_file_path", return_value="/mock/path/temp_env_vars.env"), \
         patch("builtins.open") as mock_open, \
         patch("uvicorn.run") as mock_run:

        ui(
            host="0.0.0.0",
            port=9000,
            workers=4,
            reload=True,
            docs=False,
            appdir="/tmp/appdir",
            database_uri="sqlite:///db.sqlite",
            upgrade_database=True
        )

        # Verify get_env_file_path was called and open was used
        mock_open.assert_called_once_with("/mock/path/temp_env_vars.env", "w")

        # Verify the file was written to

        # Verify uvicorn.run call
        mock_run.assert_called_once_with(
            "autogenstudio.web.app:app",
            host="0.0.0.0",
            port=9000,
            workers=4,
            reload=True,
            reload_excludes=["**/alembic/*", "**/alembic.ini", "**/versions/*"],
            env_file="/mock/path/temp_env_vars.env",
        )

def test_ui_auth_config_success():
    """Test the ui command with an existing auth config."""
    with patch("autogenstudio.cli.os.path.exists", return_value=True), \
         patch("autogenstudio.cli.get_env_file_path", return_value="/mock/path/temp_env_vars.env"), \
         patch("builtins.open") as mock_open, \
         patch("uvicorn.run") as mock_run:

        ui(auth_config="mock_config.yaml")

        # Verify get_env_file_path was called and open was used
        mock_open.assert_called_once_with("/mock/path/temp_env_vars.env", "w")

        # Verify uvicorn.run call
        mock_run.assert_called_once_with(
            "autogenstudio.web.app:app",
            host="127.0.0.1",
            port=8081,
            workers=1,
            reload=False,
            reload_excludes=None,
            env_file="/mock/path/temp_env_vars.env",
        )

def test_ui_auth_config_not_found():
    """Test the ui command with a missing auth config raises typer.Exit."""
    with patch("autogenstudio.cli.os.path.exists", return_value=False):
        with pytest.raises(typer.Exit) as exc_info:
            ui(auth_config="missing.yaml")
        assert exc_info.value.exit_code == 1
