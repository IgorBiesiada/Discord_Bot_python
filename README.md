# Discord Music Bot

A Discord bot built with Python and `nextcord` to play music from YouTube links and local files in voice channels.

## Features

- Join and leave voice channels
- Play audio from YouTube URLs, local files, and streams
- Adjust playback volume
- Stop playback and disconnect
- Simple help command using a slash command

## Prerequisites

Ensure you have the following installed:

- Python 3.6 or higher
- `nextcord` library
- `youtube_dl` library (or alternatively, `yt-dlp`)

## Setting Up Your Bot on Discord

To create your own bot and invite it to your server:

1. **Create a Discord Bot Application**:
   - Go to the [Discord Developer Portal](https://discord.com/developers/applications).
   - Click on **New Application** and give your bot a name.
   - Go to **Bot** in the sidebar, then click **Add Bot** and confirm.

2. **Retrieve Your Bot Token**:
   - Under the **Bot** settings, click **Reset Token** to generate your bot's token.
   - Copy this token. **Do not share this token with anyone**, as it gives access to your bot.

3. **Invite the Bot to Your Server**:
   - In the **OAuth2** section, select **URL Generator**.
   - Under **Scopes**, check the box for `bot`.
   - Under **Bot Permissions**, select the permissions you need. For this bot, you’ll need:
     - `Send Messages`
     - `Connect`
     - `Speak`
     - (Optional) `Use Slash Commands` for the help command.
   - Copy the generated **OAuth2 URL** at the bottom.
   - Open this URL in a new browser tab, select your server, and invite the bot.

4. **Gather Your Server ID**:
   - Enable Developer Mode in Discord (User Settings > Advanced > Developer Mode).
   - Right-click your server's icon and select **Copy ID**.
   - Paste this ID into the `SERVER_ID` variable in the bot script.

## Bot Installation and Setup

1. **Clone this repository**:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Install required libraries**:
    ```bash
    pip install nextcord youtube_dl
    ```

    > Note: You may prefer to use `yt-dlp` instead of `youtube_dl` as it is more actively maintained. Install with:
    > ```bash
    > pip install yt-dlp
    > ```

3. **Configure the bot**:
   - Open the `bot.py` file.
   - Replace `"Here paste your bot token. Don't show this token to anyone"` with your actual bot token from the Discord Developer Portal.
   - Replace `SERVER_ID` with your Discord server’s ID (as an integer).

4. **Run the bot**:
    ```bash
    python bot.py
    ```

## Usage

### Commands

| Command                | Description                                 |
|------------------------|---------------------------------------------|
| `/join <channel>`      | Bot joins the specified voice channel       |
| `/play <filename>`     | Plays a local file in the voice channel     |
| `/yt <YouTube URL>`    | Plays audio from a YouTube link             |
| `/stream <YouTube URL>`| Streams audio without downloading           |
| `/volume <number>`     | Sets playback volume (0-100)                |
| `/stop`                | Stops playback and disconnects bot          |

### Slash Commands

| Command | Description                     |
|---------|---------------------------------|
| `/help` | Sends a help message            |

## License

This project is licensed under the MIT License.
