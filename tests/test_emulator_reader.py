from typing import Awaitable, Callable

import pytest

from gateau_desktop.emulator_reader import RAM, Byte, SocketListener
from tests.conftest import RAMLog


@pytest.mark.asyncio
async def test_send_ram_message(
    ram_log: RAMLog,
    socket_listener: SocketListener,
    send_ram: Callable[[RAM], Awaitable[None]],
):
    ram = RAM(
        frame=10,
        data=[
            Byte(location=123, value=456),
            Byte(location=234, value=567),
        ],
    )

    await send_ram(ram)

    assert ram_log.messages == [ram]


@pytest.mark.asyncio
async def test_send_multiple(
    ram_log: RAMLog,
    socket_listener: SocketListener,
    send_ram: Callable[[RAM], Awaitable[None]],
):
    ram1 = RAM(
        frame=10,
        data=[
            Byte(location=123, value=456),
            Byte(location=234, value=567),
        ],
    )

    ram2 = RAM(
        frame=11,
        data=[
            Byte(location=123, value=222),
            Byte(location=234, value=333),
        ],
    )

    await send_ram(ram1)
    await send_ram(ram2)

    assert sorted(ram_log.messages, key=lambda r: r.frame) == [ram1, ram2]
