import discord
from dotenv import load_dotenv
from os import getenv

from _bot import Bot

load_dotenv()
intents = discord.Intents.default()
bot = Bot(debug_guilds=[int(getenv("DEBUG_GUILD"))], intents=intents)


@bot.command(description="設定發送訊息頻道")
@discord.default_permissions(administrator=True)
async def set_channel(ctx: discord.ApplicationContext):
    guild: discord.Guild = ctx.guild
    channel: discord.TextChannel = ctx.channel
    if guild is None:
        await ctx.send_response(
            content="This command can only be used in a server.",
            ephemeral=True,
        )
        return
    if guild and channel:
        bot.channel_id_for_guild[guild.id] = channel.id
        await ctx.send_response(
            content=f"Set ({channel.name}) as the message channel.",
            ephemeral=True,
        )


bot.load_extension("post")
bot.run(getenv("DISCORD_BOT"))
