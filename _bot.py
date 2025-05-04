import discord


class Bot(discord.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channel_id_for_guild: dict[int, int] = {}

    async def on_ready(self):
        print(f"Logged in as {self.user}")

    async def on_guild_join(self, guild: discord.Guild):
        print(f"Joined guild {guild.name}")

    async def on_guild_remove(self, guild: discord.Guild):
        if guild.id in self.channel_id_for_guild:
            del self.channel_id_for_guild[guild.id]
        print(f"Left guild {guild.name}")
