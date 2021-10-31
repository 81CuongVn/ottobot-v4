import tanjun

from ottbot.core.utils.funcs import build_loaders


component = tanjun.Component()


@component.with_slash_command
@tanjun.as_slash_command("example", "An example slash command")
async def cmd_example(ctx: tanjun.abc.SlashContext) -> None:
    await ctx.respond("test")


load_component, unload_component = build_loaders(component)
