from twitchAPI.twitch import Twitch
import asyncio


class TwitchClipper:
    def __init__(self, client_id, client_secret):
        self.twitch = Twitch(client_id, client_secret)
        # Don't authenticate here; this will need to be done asynchronously elsewhere

    async def create_clip(self, streamer_name):
        loop = asyncio.get_running_loop()

        # Async handling for user info
        user_info = await loop.run_in_executor(None, lambda: self.twitch.get_users(logins=[streamer_name]))
        if 'data' in user_info and user_info['data']:
            user_id = user_info['data'][0]['id']

            # Async handling for stream data
            stream_data = await loop.run_in_executor(None, lambda: self.twitch.get_streams(user_id=user_id))
            if stream_data['data']:
                await asyncio.sleep(60)
                clip_response = await loop.run_in_executor(None, lambda: self.twitch.create_clip(broadcaster_id=user_id,
                                                                                                 has_delay=True))
                await asyncio.sleep(10)
                return "https://clips.twitch.tv/" + clip_response['data'][0]['id']
        return None

    async def authenticate_app(self):
        # Call the authenticate_app method
        await self.twitch.authenticate_app([])
