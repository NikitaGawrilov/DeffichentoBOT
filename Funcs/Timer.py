import asyncio
import discord
from discord.ext import commands

class Timer:
    def __init__(self, timeout, callback):
        self._timeout = timeout
        self._callback = callback
        self._task = asyncio.ensure_future(self._job())

    async def _job(self):
        await asyncio.sleep(self._timeout)
        await self._callback()

    def cancel(self):
        self._task.cancel()




async def timeout_callback(): #сомнительной необходимости вещь:
    await asyncio.sleep(0.1)
    print("timeout")
    # await msg.edit(content="Время вышло!", components=[])
    return