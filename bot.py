import discord
from discord.ext import commands
import requests

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Бот запущен как {bot.user}")

@bot.command()
async def roblox(ctx, username: str):
    await ctx.send("🔍 Ищу аккаунт...")

    # Новый API поиска Roblox
    url = "https://users.roblox.com/v1/usernames/users"
    body = {
        "usernames": [username],
        "excludeBannedUsers": False
    }

    response = requests.post(url, json=body).json()

    # Пользователь не найден
    if len(response["data"]) == 0:
        return await ctx.send("❌ Аккаунт не найден!")

    user = response["data"][0]
    user_id = user["id"]
    display_name = user["displayName"]
    name = user["requestedUsername"]

    # Получаем аватар
    avatar_url = f"https://thumbnails.roblox.com/v1/users/avatar?userIds={user_id}&size=420x420&format=Png"

    avatar_data = requests.get(avatar_url).json()
    avatar = avatar_data["data"][0]["imageUrl"]

    embed = discord.Embed(
        title=f"{display_name} (@{name})",
        description=f"**User ID:** `{user_id}`",
        color=discord.Color.green()
    )
    embed.set_thumbnail(url=avatar)

    await ctx.send(embed=embed)

import os

token = os.getenv("BOT_TOKEN")

print("🔍 TOKEN CHECK:", token)
