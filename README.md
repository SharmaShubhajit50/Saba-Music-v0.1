# Saba-Music-v0.1
for dev test case, use case, post deploy test, trial &amp; error


# 🎵 Saba Music Bot

Saba Music is a **premium Discord music bot** that brings a full-featured music experience to your server. Stream songs from YouTube instantly, manage queues, and control playback with interactive buttons and slash commands. Designed to be intuitive, responsive, and visually appealing with rich embeds, Saba Music is perfect for server entertainment.  

> **Product of [Dot.Tech]**

---

## Features

- **Play Music**: Stream music from YouTube with search or direct links.  
- **Queue System**: Add multiple songs to a server-specific queue.  
- **Interactive Playback Buttons**: Pause, resume, and stop music via Discord buttons.  
- **Slash Commands**: All commands available as modern Discord slash commands.  
- **Now Playing Embeds**: Shows song title, author, duration, and requester.  
- **Finished Song Embed**: Retains details after song completion; buttons disappear automatically.  
- **Theme Customization**: Change embed color per server with `/theme`.  
- **Auto Disconnect**: Leaves voice channels after 15 minutes of inactivity. -> Still working on it(On going).  
- **Animated Status**: Bot rotates between statuses for dynamic presence.  
- **Keep Alive**: Runs with Flask server for hosting on platforms like Repl.it.  

---

## Commands

### 🎧 Music Controls
| Command | Description |
|---------|-------------|
| `/play <song>` | Play a song or add it to the queue. |
| `/stop` | Stop music and disconnect from voice channel. |
| `/skip` | Skip the currently playing song. |
| `/pause` | Pause the current song. |
| `/resume` | Resume the paused song. |

### ⚙️ System Commands
| Command | Description |
|---------|-------------|
| `/theme <color>` | Change embed theme color (purple, red, blue, green). |
| `/help` | Show the full command menu. |

---

## Interactive Buttons

- **⏸ Pause** – Pauses currently playing music.  
- **▶️ Resume** – Resumes a paused song.  
- **⏹ Stop** – Stops playback and disconnects the bot.  

**Notes:**  
- Buttons disappear automatically after the song finishes (`view=None`).  
- Now Playing embeds retain song title, author, duration, and requester.  

---

## Example Embed (Now Playing) 👇

<img width="598" height="242" alt="Annotation 2026-02-19 180847" src="https://github.com/user-attachments/assets/ae792ba9-9bcb-48f4-94a8-544f397d874b" />

## Example Embed (Finished Playing) 👇

<img width="620" height="243" alt="Annotation 2026-02-19 181016" src="https://github.com/user-attachments/assets/1cfde545-d363-4a40-8c0b-e4f8e9be0bbc" />

## Example Embed (Buttons) 👇

<img width="280" height="35" alt="Annotation 2026-02-19 181259" src="https://github.com/user-attachments/assets/9b5b6f1f-60dd-491a-9447-2a474c8b9eb3" />


## Contribution

- Contributions are welcome! You can:
- Add new commands or features.
- Improve the queue or embed system.
- Report bugs or suggest improvements.
**Submit pull requests or issues on this repository.**

## Links

- Invite Bot: <https://discord.com/oauth2/authorize?client_id=1473831371037347994&permissions=2184300608&integration_type=0&scope=bot+applications.commands>
- Support Server: <https://discord.gg/yJmAjGcu>
- Website: coming soon...


