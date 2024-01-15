import asyncio
from firebase_config import initialize_firebase
from twitch_integration import TwitchClipper
from discord_integration import DiscordBot

# Function to get user input for session_id and competitor_name

streamers = ["harabla", "aeroscoop"]  # Add streamer names here


# Function to get user input for session_id and competitor_name
def get_user_input():
    session_id = input("Enter the session ID: ")
    competitor_name = input("Enter the competitor name: ")
    return session_id, competitor_name
# Async function to monitor Firebase and create clips
async def monitor_firebase(firebase_ref, twitch_clipper, discord_bot):
    last_known_incident_amount = None
    last_known_position = None

    while True:
        data = firebase_ref.get()
        incident_amount = data.get('Player car incident amount')
        position = data.get('Position')

        if incident_amount != last_known_incident_amount or position != last_known_position:
            last_known_incident_amount = incident_amount
            last_known_position = position
            # Trigger actions when a change is detected
            for streamer in streamers:
                clip_url = await twitch_clipper.create_clip(streamer)
                if clip_url:
                    await discord_bot.post_message(YOUR_DISCORD_CHANNEL_ID, clip_url)
        await asyncio.sleep(10)  # Polling interval

# Main async function
async def main():
    session_id, competitor_name = get_user_input()
    firebase_ref = initialize_firebase(session_id, competitor_name)

    twitch_clipper = TwitchClipper("p1xzu1buwgztf4s7bquoo3wttex7ce", "iqjnjd83vul1en9toha7v0i0psbkno")
    await twitch_clipper.authenticate_app()

    discord_bot = DiscordBot('MTE5NjM3ODA3Mjc3ODI5MzI1OA.G4-OwY.klLAyCa-EmtwYPXF6OjbM-L4lHzNbgjhKXCX9g')
    # Assuming DiscordBot has an async method to start the bot
    # Start the discord bot and the firebase monitor in parallel
    await asyncio.gather(
        discord_bot.start_bot(),  # This should be an async method to start the Discord bot
        monitor_firebase(firebase_ref, twitch_clipper, discord_bot)
    )


if __name__ == "__main__":
    asyncio.run(main())
