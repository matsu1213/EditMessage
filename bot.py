import discord
import aiohttp
import os
import json
from discord.ext import commands
from dotenv import load_dotenv

# .envファイルの読み込み
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # メッセージ内容の取得を許可

bot = commands.Bot(command_prefix="!", intents=intents)

async def analyze_toxicity(text: str) -> float:
    """Perspective API を使用してメッセージのTOXICスコアを取得"""
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    headers = {"Content-Type": "application/json"}
    data = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
        "key": PERSPECTIVE_API_KEY
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            if response.status == 200:
                result = await response.json()
                return result["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
            else:
                print(f"APIエラー: {response.status}")
                return 0.0

@bot.event
async def on_ready():
    print(f"ログイン完了: {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return  # Botのメッセージは無視

    toxicity_score = await analyze_toxicity(message.content)

    if toxicity_score >= 0.3:
        try:
            await message.delete()
            await message.channel.send(f"{message.author.mention} 不適切な発言のため、メッセージが削除されました。（TOXICスコア: {toxicity_score:.2f}）", delete_after=5)
        except discord.Forbidden:
            print("削除権限がありません")
        except discord.HTTPException as e:
            print(f"削除エラー: {e}")

    await bot.process_commands(message)

bot.run(DISCORD_TOKEN)
