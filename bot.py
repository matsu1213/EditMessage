import discord
from discord import app_commands
import os
from dotenv import load_dotenv

# .envファイルの読み込み
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))

class MyBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        guild = discord.Object(id=GUILD_ID)
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)

bot = MyBot()

@bot.event
async def on_ready():
    print(f'ログイン完了: {bot.user}')

@bot.tree.command(name="edit_message", description="指定したメッセージを編集します")
@app_commands.describe(
    channel_id="編集したいメッセージがあるチャンネルのID",
    message_id="編集したいメッセージのID",
    new_content="メッセージの新しい内容"
)
async def edit_message(interaction: discord.Interaction, channel_id: str, message_id: str, new_content: str):
    # 実行者の権限をチェック
    if not interaction.user.guild_permissions.manage_messages:
        await interaction.response.send_message("このコマンドを実行するには「メッセージの管理」権限が必要です。", ephemeral=True)
        return

    try:
        # チャンネルとメッセージの取得
        channel = bot.get_channel(int(channel_id))
        if not isinstance(channel, discord.TextChannel):
            await interaction.response.send_message("指定されたチャンネルが見つかりません。", ephemeral=True)
            return

        message = await channel.fetch_message(int(message_id))
        await message.edit(content=new_content)
        
        await interaction.response.send_message("メッセージを編集しました。", ephemeral=True)
    
    except discord.NotFound:
        await interaction.response.send_message("指定されたメッセージが見つかりません。", ephemeral=True)
    except discord.Forbidden:
        await interaction.response.send_message("Botにメッセージを編集する権限がありません。", ephemeral=True)
    except Exception as e:
        print(f"エラー: {e}")
        await interaction.response.send_message("メッセージの編集に失敗しました。", ephemeral=True)

bot.run(TOKEN)