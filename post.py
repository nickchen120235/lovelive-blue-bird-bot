import dotenv
import json
import os
import twikit
from discord.ext import commands, tasks

from _bot import Bot

dotenv.load_dotenv()
client = twikit.Client(language="ja-JP")


async def get_new_posts() -> list[str]:
    try:
        client.load_cookies("./cookies.json")
        user, _ = await client.v11.settings()
        print(f"Logged in as @{user['screen_name']}")
    except:
        print("Try login with username and password")
        login = json.loads(os.environ.get("TWITTER_LOGIN", "{}"))
        try:
            await client.login(**login)
            user, _ = await client.v11.settings()
            print(f"Logged in as @{user['screen_name']}")
            client.save_cookies("./cookies.json")
        except Exception as e:
            print(e)
            print("Login failed")
            return
    finally:
        try:
            with open("./latest_tweet_id", "r") as f:
                latest_tweet_id = f.read().strip()
            print(f"Latest tweet id: {latest_tweet_id}")
            return_tweet = True
        except FileNotFoundError:
            latest_tweet_id = "0"
            return_tweet = False
            print("No latest tweet id found")
        new_tweets: list[twikit.Tweet] = []
        t_list = await client.get_list("1918527231946834405")
        for t in await t_list.get_tweets():
            if t.id > latest_tweet_id:
                new_tweets.append(t)
        if len(new_tweets) > 0:
            print(f"Found {len(new_tweets)} new tweets")
            with open("./latest_tweet_id", "w") as f:
                f.write(str(new_tweets[0].id))
        return list(reversed([f"https://x.com/{t.user.screen_name}/status/{t.id}" for t in new_tweets])) if return_tweet else []


class PostCog(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.job.start()

    def cog_unload(self):
        self.job.stop()

    @tasks.loop(seconds=30)
    async def job(self):
        posts = await get_new_posts()
        if len(posts) > 0:
            for channel_id in self.bot.channel_id_for_guild.values():
                channel = self.bot.get_channel(channel_id)
                if channel is not None:
                    for url in posts:
                        await channel.send(url)
                else:
                    print(f"Channel {channel_id} not found")

    @job.before_loop
    async def before_job(self):
        await self.bot.wait_until_ready()


def setup(bot: Bot):
    bot.add_cog(PostCog(bot))
