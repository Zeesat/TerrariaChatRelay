import discord
from dotenv import load_dotenv
import os
import asyncio
import threading 
import subprocess
import time

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

def baca_log():
    global cooldown, lines
    with open("terraria.log", "r", encoding="utf-8", errors="ignore") as f:
        f.seek(0, os.SEEK_END)
        while True:
        #    if cooldown is False:
                line = f.readline()
                if line:
                    asyncio.run_coroutine_threadsafe(
                        kirim_ke_discord(line.strip()),
                        client.loop
                    )
                    cooldown = True
                    lines = []
                else:
                    time.sleep(0.1)
                    
            # else:
            #     line = f.readline()
            #     if line:
            #         lines.append(line.strip())
            #     else:
            #         time.sleep(0.1)

                


def baca_discord():


@client.event
async def on_ready():
    print(f"Login sebagai {client.user}")



    threading.Thread(target=baca_log, daemon=True).start()
    threading.Thread(target=terminal_input, daemon=True).start()
   # threading.Thread(target=cooldown_timer, daemon=True).start()
    
client.run(DISCORD_TOKEN)
