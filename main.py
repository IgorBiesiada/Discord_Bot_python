import asyncio
import youtube_dl
import nextcord
from nextcord.ext import commands

# Configure youtube_dl options for audio extraction
ytdl_format_option = {
    'format': 'bestaudio/best',  # Extract only the best audio quality
    'outtmpl': "%(extractor)s-%(id)s-%(title)s.%(ext)s",  # Naming pattern for saved files
    'restrictfilenames': True,   # Restrict filenames to ASCII for easier compatibility
    'noplaylist': False,  # Allow playlists
    'nocheckcertificate': True,  # Ignore SSL certificate errors
    'ignoreerrors': False,  # Stop on errors
    'logtostderr': False,  # Don't log to stderr
    'quiet': True,  # Suppress unnecessary output
    'no_warnings': True,  # Suppress warnings
    'default_search': 'auto',  # Default search mode
    'source_address': '0.0.0.0',  # Bind to IPv4
}

ffmpeg_option = {'options': '-vn'}  # FFmpeg options to process audio only

# Set up YoutubeDL with the configured options
ytdl = youtube_dl.YoutubeDL(ytdl_format_option)

class YTDLSource(nextcord.PCMVolumeTransformer):
    # Class to handle audio streaming from YouTube URLs
    def __init__(self, source, *, data, volume=1):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')  # Get title of the video
        self.url = data.get('url')  # Get URL of the video

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        # Download or stream video using youtube_dl and convert it for playback
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:  # Handle playlists by selecting the first entry
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(nextcord.FFmpegPCMAudio(filename, **ffmpeg_option), data=data)

class Music(commands.Cog):
    # Class for music-related commands
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx, *, channel: nextcord.VoiceChannel=None):
        
    # If no channel is specified, use the author's current voice channel
        if channel is None:
            if ctx.author.voice:
                channel = ctx.author.voice.channel
            else:
                await ctx.send("You need to be in a voice channel or specify one.")
                return

        # If the bot is already connected, move to the new channel
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.command()
    async def play(self, ctx, *, query):
        # Command to play audio from a local file
        source = nextcord.PCMVolumeTransformer(nextcord.FFmpegPCMAudio(query))
        ctx.voice_client.play(source, after=lambda e: print(f'Player error: {e}') if e else None)
        await ctx.send(f'Playing: {query}')

    @commands.command()
    async def yt(self, ctx, *, url):
        # Command to play audio from a YouTube URL
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
        await ctx.send(f'Now playing: {player.title}')

    @commands.command()
    async def stream(self, ctx, *, url):
        # Command to stream audio directly from a YouTube URL
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
        await ctx.send(f'Now streaming: {player.title}')

    @commands.command()
    async def volume(self, ctx, volume: int):
        # Command to adjust the playback volume
        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")
        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Changed volume to {volume}%")

    @commands.command()
    async def stop(self, ctx):
        # Command to stop and disconnect the bot from voice
        await ctx.voice_client.disconnect()

    @play.before_invoke
    @yt.before_invoke
    @stream.before_invoke
    async def ensure_voice(self, ctx):
        # Ensures the bot is connected to a voice channel before playing audio
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

intents = nextcord.Intents.default()
intents.message_content = True  # Necessary for message content commands

bot = commands.Bot(
    command_prefix="/", description="Relatively simple music bot example", intents=intents
)

SERVER_ID = 1234  # Replace with your Discord server ID

@bot.slash_command(description="you can write here what you want", guild_ids=[SERVER_ID])
async def help(interaction: nextcord.Interaction):
    # Simple slash command to offer help
    await interaction.response.send_message("How can I help you?")

bot.add_cog(Music(bot))  # Register the music cog
bot.run("")  # Run the bot with your token
