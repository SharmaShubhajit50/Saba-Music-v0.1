import static_ffmpeg
static_ffmpeg.add_paths()

import os
import asyncio
import discord
import yt_dlp
from discord.ext import commands, tasks
from discord import app_commands
from dotenv import load_dotenv
from flask import Flask
from threading import Thread

# =======================
# Making a Fake server 👇
# =======================

app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()


# =========================
# LOAD TOKEN 👇
# =========================
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# =========================
# INTENTS 👇
# =========================
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True   # 🔥 Required for music

bot = commands.Bot(command_prefix="!", intents=intents)

# =========================
# GLOBAL THEME SYSTEM 👇
# =========================
DEFAULT_COLOR = discord.Color.from_rgb(155, 89, 182)
guild_themes = {}

def get_theme(guild_id):
    return guild_themes.get(guild_id, DEFAULT_COLOR)


# =========================
# AUTO DISCONNECT SYSTEM 👇
# =========================
last_activity = {}


# =========================
# GLOBAL QUEUE SYSTEM 👇
# =========================
guild_queues = {}  # {guild_id: [song_dict, ...]}



# =========================
# YTDL CONFIG 👇
# =========================
ytdl_format_options = {
    "format": "bestaudio/best",
    "quiet": True,
    "no_warnings": True,
    "extract_flat": "in_playlist",
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "source_address": "0.0.0.0",
}

ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn',
}

ytdl = yt_dlp.YoutubeDL(ytdl_format_options)

# =========================
# ANIMATED STATUS 👇
# =========================
status_list = [
    ("listening", "/play music"),
    ("watching", "Dot.Tech"),
    ("listening", "Saba Music 🎵"),
]

@tasks.loop(seconds=15)
async def change_status():
    while True:
        for status_type, text in status_list:
            if status_type == "listening":
                activity = discord.Activity(
                    type=discord.ActivityType.listening,
                    name=text
                )
            else:
                activity = discord.Activity(
                    type=discord.ActivityType.watching,
                    name=text
                )

            await bot.change_presence(activity=activity)
            await asyncio.sleep(15)


# =========================
# READY EVENT 👇
# =========================
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

    try:
        synced = await bot.tree.sync()
        print(f"Slash commands synced: {len(synced)}")
    except Exception as e:
        print(f"Error syncing commands: {e}")
    if not change_status.is_running():
        change_status.start()
    if not afk_check.is_running():
        afk_check.start()


# =========================
# BUTTON VIEW 👇
# =========================
class HelpView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        self.add_item(discord.ui.Button(
            label="Invite Bot",
            style=discord.ButtonStyle.link,
            url="https://discord.com/oauth2/authorize?client_id=1473831371037347994&permissions=2184300608&integration_type=0&scope=bot+applications.commands"
        ))

        self.add_item(discord.ui.Button(
            label="Support Server",
            style=discord.ButtonStyle.link,
            url="https://discord.gg/yJmAjGcu"
        ))

        self.add_item(discord.ui.Button(
            label="Website",
            style=discord.ButtonStyle.link,
            url="https://dottech.dev"
        ))


class PlayControls(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        # Song Pasue 
    @discord.ui.button(label="⏸ Pause", style=discord.ButtonStyle.secondary)
    async def pause_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        vc = interaction.guild.voice_client
        if vc and vc.is_playing():
            vc.pause()
            await interaction.response.send_message("⏸ Music Paused", ephemeral=True)
        else:
            await interaction.response.send_message("❌ No music is playing to pause.", ephemeral=True)

    # Song Resume 
    @discord.ui.button(label="▶️ Resume", style=discord.ButtonStyle.success)
    async def resume_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        vc = interaction.guild.voice_client
        if vc and vc.is_paused():
            vc.resume()
            await interaction.response.send_message("▶️ Music Resumed", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Music is not paused.", ephemeral=True)

    # Song Stop
    @discord.ui.button(label="⏹ Stop", style=discord.ButtonStyle.danger)
    async def stop_button(self, interaction: discord.Interaction, button: discord.ui.Button):

        vc = interaction.guild.voice_client

        if vc:
            vc.stop()
            await vc.disconnect()

            button.disabled = True
            button.label = "Stopped"
            await interaction.response.edit_message(view=self)

        else:
            await interaction.response.send_message(
                "❌ Bot is not in a voice channel.",
                ephemeral=True
            )



# =========================
# HELP COMMAND 👇
# =========================
@bot.tree.command(name="help", description="Show all Saba Music commands")
async def help_command(interaction: discord.Interaction):

    theme_color = get_theme(interaction.guild.id)

    embed = discord.Embed(
        title="🎵 Saba Music",
        description="✨ Premium Slash Music Experience\n> A Product of **Dot.Tech**",
        color=theme_color
    )

    embed.add_field(
        name="🎧 Music Controls",
        value=(
            "▶️ `/play <song>` • Play a song or link\n"
            "⏹ `/stop` • Stop & leave voice\n"
            "⏭ `/skip` • Skip song\n"
            "⏸ `/pause` • Pause playing song\n"
            "▶️ `/resume` • Resume paused song\n"
        ),
        inline=False
    )

    embed.add_field(
        name="⚙️ System",
        value=(
            "🎨 `/theme` • Change server theme color\n"
            "ℹ️ `/help` • Show this menu"
        ),
        inline=False
    )

    embed.set_thumbnail(url=interaction.client.user.display_avatar.url)
    embed.set_footer(text="Saba Music v1.0 • Elevate Your Server 🎶")

    await interaction.response.send_message(embed=embed, view=HelpView())

# =========================
# THEME COMMAND 👇
# =========================
@bot.tree.command(name="theme", description="Change embed theme color")
@app_commands.describe(color="Choose a color: purple, red, blue, green")
async def theme(interaction: discord.Interaction, color: str):

    color_map = {
        "purple": discord.Color.purple(),
        "red": discord.Color.red(),
        "blue": discord.Color.blue(),
        "green": discord.Color.green(),
    }

    if color.lower() not in color_map:
        await interaction.response.send_message(
            "❌ Invalid color. Choose: purple, red, blue, green",
            ephemeral=True
        )
        return

    guild_themes[interaction.guild.id] = color_map[color.lower()]

    await interaction.response.send_message(
        f"✅ Theme changed to {color}!",
        ephemeral=True
    )

# ================================================
# PLAY COMMAND (Queue Enabled + Finished Embed) 👇
# ================================================
@bot.tree.command(name="play", description="Play a song from YouTube")
@app_commands.describe(query="Song name or YouTube link")
async def play(interaction: discord.Interaction, query: str):

    await interaction.response.defer()
    print(f"Play command received! Query: {query}")

    if not interaction.user.voice:
        await interaction.followup.send("❌ Join a voice channel first.")
        return

    channel = interaction.user.voice.channel
    guild_id = interaction.guild.id

    if guild_id not in guild_queues:
        guild_queues[guild_id] = []

    if interaction.guild.voice_client is None:
        try:
            print(f"🔍 Searching YouTube for: {query}...")
            info = ytdl.extract_info(f"ytsearch:{query}", download=False)["entries"][0]
            url = info["url"]
            title = info["title"]

            source = discord.FFmpegPCMAudio(url, **ffmpeg_options)
        
            if vc.is_playing():
                vc.stop()
            
            vc.play(source)
            print(f"🎶 Playing: {title}")
            
            await interaction.followup.send(f"🎵 Now Playing: **{title}**")
    
        except Exception as e:
            print(f"❌ Playback Error: {e}")
            await interaction.followup.send(f"⚠️ Facing problem to play the song. Working on it. Hold tight...")

            # last uupdate
            vc = await channel.connect(self_deaf=True, timeout=60.0, reconnect=True)
        except asyncio.TimeoutError:
            return await interaction.followup.send("❌retrying, delayed in connecting to vc.")
    else:
        vc = interaction.guild.voice_client # last uupdate

    # extract info
    info = ytdl.extract_info(f"ytsearch:{query}", download=False)["entries"][0]
    url = info["url"]
    title = info["title"]
    duration = info.get("duration", 0)
    uploader = info.get("uploader", "Unknown Author")
    requester = interaction.user.mention

    minutes = duration // 60
    seconds = duration % 60
    duration_formatted = f"{minutes}:{seconds:02}"

    # add to queue
    guild_queues[guild_id].append({
        "title": title,
        "url": url,
        "requester": requester,
        "author": uploader,
        "duration": duration_formatted
    })

    if vc.is_playing():
        await interaction.followup.send(f"✅ `{title}` added to queue.")
        return

    ffmpeg_options = {
        "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
        "options": "-vn"
    }

    message_holder = {"message": None}  # to store message reference for after_playing

    async def play_next():
        if guild_queues[guild_id]:
            current = guild_queues[guild_id][0]
            # source = await discord.FFmpegOpusAudio.from_probe(current["url"], executable="ffmpeg", **ffmpeg_options)
            source = discord.FFmpegPCMAudio(url, **ffmpeg_options)
            source = discord.PCMVolumeTransformer(source)
            vc.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(after_playing(), bot.loop))

            embed = discord.Embed(
                title="🎵 Now Playing",
                description=(
                    f"`{current['title']}`\n\n"
                    f"👨‍🎤 Author: `{current['author']}`\n"
                    f"⏱ Duration: [`{current['duration']}`]\n"
                    f"🙋 Requested by: {current['requester']}"
                ),
                color=get_theme(interaction.guild.id)
            )
            embed.set_thumbnail(url="https://lottie.host/6097b269-f22f-42be-ad3b-7b022c918961/sAHuiHZTZB.lottie")

            if message_holder["message"] is None:
                message_holder["message"] = await interaction.followup.send(embed=embed, view=PlayControls())
            else:
                await message_holder["message"].edit(embed=embed, view=PlayControls())

        else:
            # Here it has been modified so that the details are retained.⬇️
            # taking the information from the previously sent embed.
            if message_holder["message"]:
                old_embed = message_holder["message"].embeds[0]
                
                finished_embed = discord.Embed(
                    title="✅ Finished Playing",
                    description=old_embed.description, # retain the song and the author's name.
                    color=discord.Color.green()
                )
                finished_embed.set_footer(text="✅ Song completed successfully.")
                
                # set the view to 'None', the buttons will disappear when the song ends.
                await message_holder["message"].edit(embed=finished_embed, view=None)

    async def after_playing():
        # remove finished song
        if guild_queues[guild_id]:
            guild_queues[guild_id].pop(0)
        await play_next()

    await play_next()


# =========================
# STOP COMMAND 👇
# =========================
@bot.tree.command(name="stop", description="Stop music and leave")
async def stop(interaction: discord.Interaction):

    if interaction.guild.voice_client:
        await interaction.guild.voice_client.disconnect()
        await interaction.response.send_message("⏹ Music stopped.")
    else:
        await interaction.response.send_message("❌ Bot is not in a voice channel.")


@tasks.loop(minutes=1)
async def afk_check():

    now = asyncio.get_event_loop().time()

    for guild in bot.guilds:
        vc = guild.voice_client

        if vc and not vc.is_playing():

            last = last_activity.get(guild.id, now)

            if now - last > 900:  # 15 minutes
                await vc.disconnect()
                print(f"Auto disconnected from {guild.name} due to inactivity.")


# =========================
# SKIP COMMAND 👇
# =========================
@bot.tree.command(name="skip", description="Skip the currently playing song")
async def skip(interaction: discord.Interaction):

    vc = interaction.guild.voice_client
    if not vc or not vc.is_playing():
        await interaction.response.send_message("❌ No song is currently playing.", ephemeral=True)
        return

    if interaction.guild.id in guild_queues and guild_queues[interaction.guild.id]:
        skipped_song = guild_queues[interaction.guild.id][0]["title"]
        vc.stop()
        await interaction.response.send_message(f"⏭ Skipped `{skipped_song}`.")
    else:
        await interaction.response.send_message("❌ Queue is empty.", ephemeral=True)



# =========================
# PAUSE COMMAND 👇
# =========================
@bot.tree.command(name="pause", description="Pause the current song")
async def pause(interaction: discord.Interaction):
    vc = interaction.guild.voice_client
    if vc and vc.is_playing():
        vc.pause()
        await interaction.response.send_message("⏸ Music has been paused.")
    else:
        await interaction.response.send_message("❌ No music is playing.", ephemeral=True)



# =========================
# RESUME COMMAND 👇
# =========================
@bot.tree.command(name="resume", description="Resume the paused song")
async def resume(interaction: discord.Interaction):
    vc = interaction.guild.voice_client
    if vc and vc.is_paused():
        vc.resume()
        await interaction.response.send_message("▶️ Music has been resumed.")
    else:
        await interaction.response.send_message("❌ Music is not paused.", ephemeral=True)


keep_alive()

# =========================
# RUN 👇
# =========================
bot.run(TOKEN)


