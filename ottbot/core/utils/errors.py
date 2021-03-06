# TODO: Update error handler

import typing as t

import hikari
import tanjun

from ottbot.abc.ibot import IBot
from ottbot.abc.iclient import IClient


class Doneions(Exception):
    """Error Level that will personally email me if this ever triggers"""

    def __init__(self, message: str = "") -> None:
        self._email()
        super().__init__(message)

    def _email(self) -> None:
        ...


class NGonError(Exception):
    """Error level above critical"""

    ...


class Errors:
    def __init__(self, bot: IBot):
        self.bot = bot

    def embed(self, ctx: tanjun.abc.Context, message: str) -> t.Optional[hikari.Embed]:
        assert isinstance(ctx.client, IClient)
        desc = f"❌ {message}"

        embed = self.bot.embeds.build(ctx=ctx, description=desc, footer="None")

        return embed

    @staticmethod
    def ngon(message: str) -> NGonError:
        """Create an extreemly important error"""
        return NGonError(message)
