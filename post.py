import asyncio
import dotenv
import json
import os
import twikit

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


async def main():
    print(await get_new_posts())
asyncio.run(main())
