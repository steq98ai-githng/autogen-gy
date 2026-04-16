import asyncio
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import grpc
import pytest
from autogen_ext.runtimes.grpc._worker_runtime import HostConnection
from grpc.aio import AioRpcError


@pytest.mark.asyncio
async def test_connect_read_loop_exception() -> None:
    # Setup mock stream and stub
    mock_stream = MagicMock()
    mock_stream.wait_for_connection = AsyncMock()

    # Create an AioRpcError using correct arguments for a simulated test
    aio_error = AioRpcError(
        code=grpc.StatusCode.UNAVAILABLE,
        initial_metadata=grpc.aio.Metadata(),
        trailing_metadata=grpc.aio.Metadata(),
        details="Simulated network error",
        debug_error_string="simulated",
    )

    # First call throws error
    mock_stream.read = AsyncMock(side_effect=[aio_error])

    mock_stub = MagicMock()
    mock_stub.OpenChannel.return_value = mock_stream

    send_queue: asyncio.Queue[Any] = asyncio.Queue()
    recv_queue: asyncio.Queue[Any] = asyncio.Queue()

    # Call _connect
    with patch("autogen_ext.runtimes.grpc._worker_runtime.logger") as mock_logger:
        task = await HostConnection._connect(mock_stub, send_queue, recv_queue, "test_client_id")  # pyright: ignore[reportPrivateUsage]

        # Wait for task to finish
        await asyncio.wait_for(task, timeout=1.0)

        # Verify logger.error was called with the AioRpcError message
        mock_logger.error.assert_called_with(f"gRPC error reading from stream: {aio_error}")


@pytest.mark.asyncio
async def test_connect_read_loop_generic_exception() -> None:
    # Setup mock stream and stub
    mock_stream = MagicMock()
    mock_stream.wait_for_connection = AsyncMock()
    generic_error = Exception("Unexpected simulated error")
    mock_stream.read = AsyncMock(side_effect=[generic_error])

    mock_stub = MagicMock()
    mock_stub.OpenChannel.return_value = mock_stream

    send_queue: asyncio.Queue[Any] = asyncio.Queue()
    recv_queue: asyncio.Queue[Any] = asyncio.Queue()

    # Call _connect
    with patch("autogen_ext.runtimes.grpc._worker_runtime.logger") as mock_logger:
        task = await HostConnection._connect(mock_stub, send_queue, recv_queue, "test_client_id")  # pyright: ignore[reportPrivateUsage]

        # Wait for task to finish
        await asyncio.wait_for(task, timeout=1.0)

        # Verify logger.error was called for the generic Exception
        mock_logger.error.assert_called_with(f"Unexpected error reading from stream: {generic_error}", exc_info=True)
