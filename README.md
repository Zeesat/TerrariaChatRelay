# Discord Bot Stolas

This project relays Discord chat with a Terraria server through server log parsing and command forwarding.

## Project Structure

```text
.
|-- .env
|-- .gitignore
|-- README.md
|-- ReLogic.Native.dll
|-- TerrariaServer.exe
|-- serverconfig.txt
|-- terraria.log
|-- scripts/
|   `-- start-server.bat
`-- src/
    |-- bot/
    |   `-- stolas_bot.py
    `-- native/
        `-- launcher.c
```

## File Placement Standard

- `src/`: all source code.
- `src/bot/`: Discord bot source (Python).
- `src/native/`: native helper source (C).
- `scripts/`: operational scripts.
- Project root: Terraria runtime files (`TerrariaServer.exe`, `ReLogic.Native.dll`, `serverconfig.txt`, `terraria.log`) to keep existing runtime paths compatible.

## Run

Run from the project root:

```bat
scripts\start-server.bat
```

Run the Discord bot:

```bat
python src\bot\stolas_bot.py
```

## Configuration

Minimum `.env` values:

```env
DISCORD_TOKEN=your_token
CHANNEL_ID=your_channel_id
```

## Notes

- This refactor changes only file and folder layout.
- Source code logic is unchanged.
