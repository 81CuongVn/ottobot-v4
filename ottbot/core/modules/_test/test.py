import random

import aiohttp
import hikari
import sake
import tanjun
from hikari.events.message_events import GuildMessageCreateEvent

from ottbot.core.bot import OttBot
from ottbot.core.utils.funcs import build_loaders, obtain_item

component, load_component, unload_component = build_loaders()


@component.with_slash_command
@tanjun.as_slash_command("hello", "Says hello!")
async def cmd_hello(ctx: tanjun.abc.SlashContext) -> None:
    greeting: str = random.choice(("Hello", "Hi", "Hey"))
    await ctx.respond(
        f"{greeting} {ctx.author.mention if ctx.member else ctx.author.username}!",
        user_mentions=True,
    )


@component.with_slash_command
@tanjun.as_slash_command("test2", "Says hello!")
async def cmd_test2(ctx: tanjun.abc.SlashContext) -> None:
    greeting: str = random.choice(("Hello", "Hi", "Hey"))
    await ctx.respond(
        f"{greeting} {ctx.author.mention if ctx.member else ctx.author.username}!",
        user_mentions=True,
    )


# @component.with_slash_command
# @tanjun.with_int_slash_option("number", "The number of dice to roll (max: 25).")
# @tanjun.with_int_slash_option("sides", "The number of sides each die will have.", default=6)
# @tanjun.with_int_slash_option("bonus", "A fixed number to add to the total roll.", default=0)
# @tanjun.as_slash_command("dice", "Roll one or more dice.")
# async def cmd_dice(ctx: tanjun.abc.SlashContext, number: int, sides: int, bonus: int) -> None:
#     if number > 25:
#         await ctx.respond("No more than 25 dice can be rolled at once.")
#         return

#     if sides > 100:
#         await ctx.respond("The dice cannot have more than 100 sides.")
#         return

#     rolls: list[int] = [random.randint(1, sides) for _ in range(number)]
#     await ctx.respond(
#         " + ".join(f"{r}" for r in rolls) + (f" + {bonus} (bonus)" if bonus else "") + f" = **{sum(rolls) + bonus:,}**"
#     )


@component.with_slash_command
@tanjun.with_str_slash_option("id_str", "The ID of the user you would like to access")
@tanjun.as_slash_command("user", "Get the name of a user give their ID")
async def cmd_user(
    ctx: tanjun.abc.SlashContext,
    id_str: str,
    bot: OttBot = tanjun.inject(type=OttBot),
) -> None:
    if ctx.guild_id is not None:
        user = bot.cache.get_member(ctx.guild_id, int(id_str))
        if user is not None:
            await ctx.respond(f"{user.mention}")
    else:
        await ctx.respond("User not found")


@component.with_slash_command
@tanjun.as_slash_command("waitfor", "`wait_for` test")
async def cmd_waitdfor(
    ctx: tanjun.abc.SlashContext,
    bot: OttBot = tanjun.inject(type=OttBot),
) -> None:
    await ctx.respond("Send a message")
    event: GuildMessageCreateEvent = await bot.wait_for(
        GuildMessageCreateEvent,
        timeout=60,
        predicate=lambda e: (
            isinstance(e, GuildMessageCreateEvent)  # event is a MessageCreateEvent
            and e.author.id == ctx.author.id  # event is from the author
        ),
    )
    await ctx.respond(f"{event.author.mention} said {event.content}")


@component.with_slash_command
@tanjun.as_slash_command("testdb", "test that the bot's database is working")
async def cmd_test_db(ctx: tanjun.abc.SlashContext, bot: OttBot = tanjun.inject(type=OttBot)) -> None:
    await bot.pool.execute(
        "INSERT INTO users (discord_id) VALUES ($1)",
        str(ctx.author.id),
    )
    _, id_ = await bot.pool.row("SELECT * FROM users WHERE discord_id = $1", str(ctx.author.id))
    usr = await bot.rest.fetch_user(int(id_))
    await ctx.respond(usr.username)
    await bot.pool.execute("DELETE FROM users WHERE discord_id = $1", str(ctx.author.id))


@component.with_slash_command
@tanjun.with_member_slash_option("member", "The member test on")
@tanjun.as_slash_command("nick_test", "test nickname permissions")
async def cmd_nick_test(
    ctx: tanjun.abc.SlashContext, member: hikari.Member, bot: OttBot = tanjun.inject(type=OttBot)
) -> None:
    await member.edit(nick="asdf")
    await member.edit(nick=hikari.UNDEFINED)
    await ctx.respond("User Updated")


@component.with_slash_command
@tanjun.as_slash_command("testobt", "Test obtain item")
async def cmd_testobt(
    ctx: tanjun.abc.SlashContext,
    sake: sake.redis.RedisCache = tanjun.inject(type=sake.redis.RedisCache),
    bot: OttBot = tanjun.inject(type=OttBot),
) -> None:
    if ctx.guild_id is None:
        return
    member = await obtain_item(hikari.Member, bot.cache, sake, bot.rest, ctx.author.id, ctx.guild_id)
    await ctx.respond(member.display_name)

    guild = await obtain_item(hikari.Guild, bot.cache, sake, bot.rest, ctx.guild_id)
    await ctx.respond(guild.name)


@component.with_slash_command
@tanjun.as_slash_command("embedtest", "description")
async def cmd_embedtest(ctx: tanjun.abc.SlashContext) -> None:
    """Send just an embed"""
    if ctx.guild_id is None:
        return

    msg = await ctx.respond(hikari.Embed(title="asdf", description="asdf"), ensure_result=True)
    await msg.edit(embed=hikari.Embed(title="asdf", description="asdf", color=0xFF0000))


@component.with_slash_command
@tanjun.as_slash_command("sessiontest", "Test the aiohttp session")
async def cmd_sessiontest(
    ctx: tanjun.abc.SlashContext, session: aiohttp.ClientSession = tanjun.inject(type=aiohttp.ClientSession)
) -> None:
    if ctx.guild_id is None:
        return

    resp = await session.get("https://my-json-server.typicode.com/AlexanderHOtt/demo/users")
    data = await resp.json()
    await ctx.respond(data)
