import discord
from dotenv import load_dotenv
import os
import asyncio
import threading 
import subprocess
import time
import re

# Wait for Terraria Server Start 
time.sleep(3)

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


async def kirim_ke_discord(pesan):
    await client.wait_until_ready()

    channel = client.get_channel(CHANNEL_ID)
    if channel is None:
        channel = await client.fetch_channel(CHANNEL_ID)

    await channel.send(pesan)

def terminal_input():
    while True:
        teks = input("> ")
        asyncio.run_coroutine_threadsafe(
                kirim_ke_discord(teks),
                client.loop
            )
    
# def cooldown_timer():
#     global cooldown, line
#     while cooldown:
#         time.sleep(0.9)
#         if lines:
#             line = "\n".join(lines)
#             asyncio.run_coroutine_threadsafe(
#                 kirim_ke_discord(line),
#                 client.loop
#             )
#             cooldown = False        
#         else:
#             cooldown = False

# cooldown = False
# lines = []   

pattern = r"^((?:\d{1,3}\.){3}\d{1,3})(:\d+)"
IGNORED_PREFIXES = (
    "Saving world data: ",
    "Resetting game objects ",
    "Loading world data: ",
    "Settling liquids ",
)

def baca_log():
    global cooldown, lines
    with open("Terraria.log", "r", encoding="utf-8", errors="ignore") as f:
        f.seek(0, os.SEEK_END)
        while True:
        #    if cooldown is False:
                line = f.readline()
                if line:
                    if line.startswith(IGNORED_PREFIXES):
                        continue
                    if line == ": \n" or line == ": " or line == ":":
                        continue
                    line = re.sub(pattern, "xxx.xxx.xxx.xxx\\2", line)
                    if ("<Server>" not in line) and ("Invalid command." not in line):
                        asyncio.run_coroutine_threadsafe(
                            kirim_ke_discord(line.strip().replace("\n", " ")),
                            client.loop
                        )
                    # cooldown = True
                    # lines = []
                else:
                    time.sleep(0.1)

            # else:
            #     line = f.readline()
            #     if line:
            #         lines.append(line.strip())
            #     else:
            #         time.sleep(0.1)

                

@client.event
async def on_ready():
    # print(f"Login as {client.user}", flush=False)
    asyncio.run_coroutine_threadsafe(
    kirim_ke_discord(f"Login as {client.user}"),
    client.loop)


    threading.Thread(target=baca_log, daemon=True).start()
   # threading.Thread(target=terminal_input, daemon=True).start()
   # threading.Thread(target=cooldown_timer, daemon=True).start()

@client.event
async def on_message(message):
    if message.author.bot:   # ignore bot msg
        return
    if message.channel.id == CHANNEL_ID:
        if message.content.startswith("!Stolas"):
            stolas_text = message.content[len("!Stolas"):].strip()
            if stolas_text:
                print(stolas_text, flush=True)
            return
        print(f"say [c/7289DA:<{message.author.display_name}>] {message.content}", flush=True)
        


client.run(DISCORD_TOKEN)
