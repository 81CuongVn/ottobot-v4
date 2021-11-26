# TODO: Update error handler

import typing as t

import hikari
import tanjun

from ottbot.abc.iclient import IClient
from ottbot.core.bot import OttBot


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
    def embed(
        self, ctx: tanjun.abc.Context, message: str, bot: OttBot = tanjun.injected(type=OttBot)
    ) -> t.Optional[hikari.Embed]:
        assert isinstance(ctx.client, IClient)
        desc: str = f"❌ {message}"

        embed: hikari.Embed = bot.embeds.build(ctx=ctx, description=desc, footer="None")

        return embed

    @staticmethod
    def ngon(message: str) -> NGonError:
        """Create an extreemly important error"""
        return NGonError(message)

    @staticmethod
    def parse(exc: Exception):
        print(exc)
        raise exc

    async def parse_tanjun(self, exc: t.Union[tanjun.CommandError, Exception], ctx: tanjun.abc.Context) -> None:
        """Parse tanjun errors"""
        if isinstance(exc, (tanjun.NotEnoughArgumentsError, tanjun.TooManyArgumentsError)):
            await ctx.respond(self.embed(ctx, f"**ERROR**```{exc.message}```"))  # type: ignore
            raise exc

        elif isinstance(exc, tanjun.MissingDependencyError):
            await ctx.respond(self.embed(ctx, f"**ERROR**```{exc.message}```"))  # type: ignore
            raise exc

        else:
            print(exc)
            raise exc
