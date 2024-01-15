import discord

class DiscordBot:
    def __init__(self, token):
        intents = discord.Intents.default()  # Enables default intents
        self.client = discord.Client(intents=intents)
        self.token = token

    async def start_bot(self):
        await self.client.start(self.token)

    async def post_message(self, channel_id, message):
        channel = self.client.get_channel(channel_id)
        await channel.send(message)
