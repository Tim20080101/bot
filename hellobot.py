import discord
import os
import random
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('HELLOBOT_TOKEN')
print("hellobot token get:", TOKEN)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="", intents=intents)

@bot.event
async def on_ready():
    print(f'HelloBot 已登入為: {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.lower() == "hello":
        greetings = [
            "Hola! (西班牙語)",
            "Bonjour! (法語)",
            "Ciao! (義大利語)",
            "Hallo! (德語)",
            "こんにちは! (日語)",
            "안녕하세요! (韓語)",
            "Hello! (英語)",
            "Olá! (葡萄牙語)"
        ]
        reply = random.choice(greetings)
        await message.channel.send(reply)
    elif message.content.lower() == "hi":
        await message.channel.send("你知道我是誰嗎")

# --- 改成 async 函數啟動 ---
async def run_bot():
    token = os.getenv('HELLOBOT_TOKEN')
    if not token:
        raise ValueError("HELLOBOT_TOKEN 沒有設定！")
    await bot.start(token)  # 注意：不要用 bot.run()
